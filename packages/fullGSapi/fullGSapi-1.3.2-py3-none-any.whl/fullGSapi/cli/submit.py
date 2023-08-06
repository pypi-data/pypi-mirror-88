import click
import os
import pathlib
import json

from fullGSapi.cli.utils import LoginTokens, course_id_option, assignment_id_option, get_tokens, getListOfFiles

@click.command()
@course_id_option
@assignment_id_option
@click.option("--method", "-m", "method", default="upload", help="The method you are using to submit.", type=click.Choice(["upload", "github", "bitbucket"]))
@click.option("--folder", "-f", "folder", default=".", help="The file or folder which you want to submit", type=click.Path())
@click.option("--repository", "-r", "repository", default=None, help="The full repository path of your repo (must include both the username and repo name).", type=str)
@click.option("--branch", "-b", "branch", default=None, help="The branch which you want to submit.", type=str)
@click.option("--email", "-e", "email", default=None, help="This option allows an instructor to submit an assignment on behalf of some student via their email.", type=str)
@click.option("--partner", "-p", "partner", default=None, help="This option allows you to add your partner or partners to the assignment right after it has been submitted. To add a partner, you must add their email address. If you would like to add multiple partners, separate them by a comma `,`. For example if I wanted to add foo@gradescope.com and bar@gradescope.com as partners, I would enter '-p foo@gradescope.com,bar@gradescope.com'.", type=str)
@click.option("--leaderboard", "-l", "leaderboard", default="", help="This is the leaderboard name which will show up on Gradescope.", type=str)
@click.option("--programming/--pdf", default=True, help="This is to set if you are submitting a programming vs PDF assignment.", type=bool)
@click.pass_context
def submit(ctx, course: str, assignment: str, method: str, folder: str, repository: str, branch: str, email: str, partner: str, leaderboard: str, programming: bool):
    """
    This allows you to submit a programming or pdf assignment. Instructors may submit on behalf of students.
    """
    
    tokens: LoginTokens = get_tokens(ctx)

    submission_id = None
    gs = tokens.gsFullapi

    # UPLOAD =================================
    if method == "upload":
        gs = tokens.gsAPI
        if programming:
            click.echo("Collecting files...")
            filenames = getListOfFiles(folder)
            files = {f[(len(str(pathlib.Path(folder).parent)) if os.path.isfile(folder) else len(folder)) + 1:]:open(f, 'rb').read() for f in filenames}
            click.echo("Uploading programming submission...")
            res = gs.upload_programming_submission(course, assignment, email, files_dict=files)
        else:
            click.echo("Uploading pdf subission...")
            res = gs.upload_pdf_submission(course, assignment, email, folder)
        if res.ok:
            click.echo("Success!")
            try:
                data = json.loads(res.content)
                submission_id = data['id']
                print(f"Submission URL: https://www.gradescope.com/courses/{course}/assignments/{assignment}/submissions/{submission_id}")
            except Exception as e:
                print(e)
                import traceback
                traceback.print_exc()
                click.echo(f"Failed to parse response: {res.content}!")
        else:
            click.echo("Failed!")
            click.echo(res.content)
        # return
    else:
        if not programming:
            click.echo("Upload is the only method which supports pdf submissions.")
            return

        if not repository:
            click.echo("You must specify a repository if you are not directly uploading files!")
            return
        if not branch:
            click.echo("You must specify the branch you want to upload from!")
            return

        if email is not None:
            res = gs.get_submission_roster(course, assignment)
            if not res:
                click.echo("Failed to fetch the roster! Are you authorized to visit that page?")
                return
            for s in res:
                if s.get("email") == email:
                    email = s["id"]
                    break
            else:
                click.echo(f"Could not find {email} in the roster!")
                return

        # GITHUB =================================
        if method == "github":
            click.echo("Checking if the repo is valid...")
            # data = gs.get_github_projects()
            # if not data:
            #     click.echo("Failed to fetch your GitHub project list! Please go to Gradescope and verify you have authenticated GitHub with your account.")
            #     return
            repo_id = None
            # for repo in data:
            #     if repo.get("full_name") == repository:
            #         repo_id = repo["id"]
            #         break
            repo = gs.find_github_project(repository)
            if repo:
                repo_id = repo["id"]
            else:
                click.echo(f"Could not find the repo {repository} in your account!")
                return
            branches = gs.get_github_branches(repo_id)
            if not branches:
                click.echo(f"Failed to fetch branches for {repository}!")
                return
            for b in branches:
                if b.get("name") == branch:
                    break
            else:
                click.echo(f"Could not find the branch '{branch}' in the repository '{repository}'!")
                return
            repository = repo_id


        # BITBUCKET ==============================
        elif method == "bitbucket":
            data = gs.get_bitbucket_projects()
            if not data:
                click.echo("Failed to fetch your BitBucket project list! Please go to Gradescope and verify you have authenticated BitBucket with your account.")
                return
            for repo in data:
                if repo.get("full_name") == repository:
                    break
            else:
                click.echo(f"Could not find the repo {repository} in your account!")
                return
            branches = gs.get_bitbucket_branches(repository)
            if not branches:
                click.echo(f"Failed to fetch branches for {repository}!")
                return
            for b in branches:
                if b.get("name") == branch:
                    break
            else:
                click.echo(f"Could not find the branch '{branch}' in the repository '{repository}'!")
                return
        click.echo("Submitting...")
        data = gs.submit_via_repo(course, assignment, method, repository, branch, leaderboard_name=leaderboard, owner_id=email)
        if data[0] or data[0] is None:
            click.echo("Submitted successfully!")
            url = data[1]
            click.echo(f"Submission URL: {url}")
            submission_id = url[len(gs.base_url + f"/courses/{course}/assignments/{assignment}/submissions/"):]
        else:
            click.echo("Submission Failed!")
            click.echo(f"Info: {data[1]}")
            return
    if partner:
        partners = partner.split(",")
        click.echo("Adding partners...")
        pdata = gs.get_groups_data_from_emails(course, assignment, submission_id, partners)
        if pdata is None:
            click.echo("Could not fetch the IDs for the partners! Are you sure the assignment allows for partners?")
            return
        if not isinstance(pdata, list):
            pdata = [pdata]
        if len(pdata) != len(partners):
            click.echo(f"Partner and partner ID length mismatch!")
            return
        for i, p in enumerate(pdata):
            if pdata[i] is False:
                s = f"! {i + 1}. Name: UNKNOWN; Email: {partners[i]} - COULD NOT FIND STUDENT! Make sure you are using their primary email on Gradescope."
            else:
                s = f"  {i + 1}. Name: {p.get('name', 'UNKNOWN')}; Email: {p.get('email')}"
            click.echo(s)
        ids = [data["id"] for data in pdata if data is not False and "id" in data]
        if not ids:
            click.echo("Could not find any students to add to your submission!")
            return
        if gs.add_group_members(course, assignment, submission_id, ids):
            click.echo("Group memebers successfully added to the submission!")
        else:
            click.echo("Failed to add group memebers to the submission!")
            return
        
