from fastapi import APIRouter, Depends, HTTPException, Path, Body, status

from schemas.github import (
    IssueCreate, PullRequestCreate, RepoQueryParams, IssueQueryParams, CommitQueryParams,RepoResponse, IssueCreateResponse,IssueResponse,CommitResponse
)

from services.github_service import get_github_service, GitHubService

router = APIRouter(prefix="/github", tags=["github"])


@router.get('/repos', response_model=RepoResponse)
async def fetch_repos(
    q: RepoQueryParams = Depends(),
    svc: GitHubService = Depends(get_github_service),
):  
    """
    Fetch repositories for a given user or organization.
    
    You must provide exactly one of either `username` or `org_name` in the query parameters.
    Supports pagination, type filtering (public, private, forks, etc.), and sorting.
    
    Raises:
        HTTPException(400): If both or neither of `username` and `org_name` are provided.
    """
    username = q.username or ''
    org_name = q.org_name or ''
    if bool(username.strip()) == bool(org_name.strip()):
        raise HTTPException(
            status_code=400,
            detail={"msg": "Provide exactly one of 'username' or 'org_name'"},
        )

    if q.username.strip():
        return await svc.get_user_repos(
            username=username,
            type=q.type,
            sort=q.sort,
            direction=q.direction,
            per_page=q.per_page,
            page=q.page,
        )

    if q.org_name.strip():
        return await svc.get_org_repos(
            org_name=org_name,
            type=q.type,
            sort=q.sort,
            direction=q.direction,
            per_page=q.per_page,
            page=q.page,
        )


@router.post("/{owner}/{repo}/issues", response_model=IssueCreateResponse)
async def new_issue(
    issue: IssueCreate = Body(...),
    owner: str = Path(...),
    repo: str = Path(...),
    svc: GitHubService = Depends(get_github_service)
):
    """
    Create a new issue in a specific repository.
    
    Accepts issue details such as title, body, labels, milestones, and assignees.
    Only the title is explicitly required. Authentication with appropriate GitHub token permissions
    is required to successfully create an issue on the target repository.
    """
    result = await svc.create_issue(owner, repo, **issue.model_dump(exclude_none=True))
    return {"message": "Issue created", "issue": result}


@router.get('/{owner}/{repo}/issues', response_model=IssueResponse)
async def get_issues(
    owner: str = Path(...),
    repo: str = Path(...),
    q: IssueQueryParams = Depends(),
    svc: GitHubService = Depends(get_github_service),
):
    """
    List issues in a specified repository.
    
    Supports filtering by issue state (open/closed/all), specific labels, and relationship 
    filters (assigned to you, created by you, mentioned, etc.). Also supports pagination
    and sorting configurations.
    """
    return await svc.list_issues(
        owner=owner,
        repo=repo,
        filter=q.issue_filter,
        state=q.state,
        labels=q.labels,
        sort=q.sort,
        direction=q.direction,
        since=q.since,
        per_page=q.per_page,
        page=q.page,
    )


@router.get("/{owner}/{repo}/commits", response_model=CommitResponse)
async def fetch_repo_commits(
    q: CommitQueryParams = Depends(),
    owner: str = Path(...),
    repo: str = Path(...),
    svc: GitHubService = Depends(get_github_service)
):
    """
    Fetch the commit history from a repository.
    
    Allows filtering by starting SHA/branch, author/committer usernames, specific file paths,
    and date ranges (since/until). This endpoint is fully paginated.
    """

    return await svc.get_commits(
        owner,
        repo,
        params=q.model_dump(exclude_none=True)
    )


@router.post("/{owner}/{repo}/pulls", response_model=dict, status_code=status.HTTP_201_CREATED)
async def new_pull_request(
    pr: PullRequestCreate,
    owner: str = Path(...),
    repo: str = Path(...),
    svc: GitHubService = Depends(get_github_service)
):
    """
    Create a new Pull Request.
    
    Requires the source branch (`head`) and the target branch (`base`). 
    You must provide either a `title` (to create a PR from scratch) OR an `issue` number 
    (to convert an existing issue into a PR).
    
    Raises:
        HTTPException(400): If you provide both or neither of `title` and `issue`.
    """

    title = pr.title
    issue = pr.issue

    has_title = bool(title and title.strip())
    has_issue = issue is not None

    if has_title == has_issue:
        raise HTTPException(
            status_code=400,
            detail={"msg": "Provide exactly one of 'title' or 'issue'"}
        )

    result = await svc.create_pull_request(
        owner, repo, **pr.model_dump(exclude_none=True)
    )
    return {"message": "PR created", "pr": result}

github_router = router
