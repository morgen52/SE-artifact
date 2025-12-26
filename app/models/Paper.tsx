interface Paper {
    paper_id: string;
    year: number;
    venue: string;
    title: string;
    code_link: string;
    language: string;
    last_update_time: string;
    paper_link: string;
    repo_name: string;
    github_star: number;
    github_fork: number;
    citation_count: number;
    github_issues: number;
    github_open_issues: number;
    github_update_date: string;
    prioritized: boolean;
}

export default Paper;