from fastapi import APIRouter, Depends, HTTPException, Path, Body, status

from schemas.github import (
    IssueCreate, PullRequestCreate, RepoQueryParams, IssueQueryParams, CommitQueryParams,Repo
)

from services.github_service import get_github_service, GitHubService

router = APIRouter(prefix="/github", tags=["github"])


@router.get('/repos', response_model=RepoResponse)
async def fetch_repos(
    q: RepoQueryParams = Depends(),
    svc: GitHubService = Depends(get_github_service),
):  
    '''
    Fetch repositories for a user or organization
    '''
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


@router.post("/{owner}/{repo}/issues", response_model=dict)
async def new_issue(
    issue: IssueCreate = Body(...),
    owner: str = Path(...),
    repo: str = Path(...),
    svc: GitHubService = Depends(get_github_service)
):
    """Create a new issue in a repository"""
    result = await svc.create_issue(owner, repo, **issue.model_dump(exclude_none=True))
    return {"message": "Issue created", "issue": result}


@router.get('/{owner}/{repo}/issues', response_model=list)
async def get_issues(
    owner: str = Path(...),
    repo: str = Path(...),
    q: IssueQueryParams = Depends(),
    svc: GitHubService = Depends(get_github_service),
):
    '''
    List issues in a repository
    '''
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


@router.get("/{owner}/{repo}/commits", response_model=list)
async def fetch_repo_commits(
    q: CommitQueryParams = Depends(),
    owner: str = Path(...),
    repo: str = Path(...),
    svc: GitHubService = Depends(get_github_service)
):
    """Fetch commits from a repository"""

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
    """Create a pull request"""

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
