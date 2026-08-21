document.addEventListener("DOMContentLoaded", async () => {
    const githubUser = "Yosskavo";
    const codebergUser = "yosskavo";

    const stats = {
        publicRepos: 0,
        totalCommits: 0,
        stars: 0,
        lastRepo: null,
        forks: []
    };

    try {
        // 1. Fetch Repos from both platforms
        const ghReposRes = await fetch(`https://api.github.com/users/${githubUser}/repos?per_page=100`);
        const ghRepos = ghReposRes.ok ? await ghReposRes.json() : [];

        const cbReposRes = await fetch(`https://codeberg.org/api/v1/users/${codebergUser}/repos`);
        const cbRepos = cbReposRes.ok ? await cbReposRes.json() : [];

        // Format repos to a common structure
        const formattedGhRepos = ghRepos.map(r => ({
            name: r.name,
            html_url: r.html_url,
            isPrivate: r.private,
            fork: r.fork,
            stars: r.stargazers_count || 0,
            updated: new Date(r.pushed_at || r.updated_at),
            source: 'GitHub'
        }));

        const formattedCbRepos = cbRepos.map(r => ({
            name: r.name,
            html_url: r.html_url,
            isPrivate: r.private,
            fork: r.fork,
            stars: r.stars_count || 0,
            updated: new Date(r.updated_at),
            source: 'Codeberg'
        }));

        const allRepos = [...formattedGhRepos, ...formattedCbRepos];

        stats.publicRepos = allRepos.filter(r => !r.isPrivate).length;
        
        allRepos.forEach(repo => {
            stats.stars += repo.stars;
            if (repo.fork) {
                stats.forks.push(repo);
            }
        });

        // 2. Find last committed repo
        if (allRepos.length > 0) {
            allRepos.sort((a, b) => b.updated - a.updated);
            stats.lastRepo = allRepos[0];
        }

        // 3. Fetch Commits Total
        // GitHub total commits (using search api, can be rate limited so fallback to basic)
        const ghCommitsRes = await fetch(`https://api.github.com/search/commits?q=author:${githubUser}`, {
            headers: { 'Accept': 'application/vnd.github.cloak-preview+json' }
        });
        const ghCommits = ghCommitsRes.ok ? await ghCommitsRes.json() : { total_count: 0 };
        stats.totalCommits += (ghCommits.total_count || 207);

        // Codeberg total commits (fetch per repo header)
        for (const repo of formattedCbRepos) {
            if (!repo.fork) {
                try {
                    const cbCommitRes = await fetch(`https://codeberg.org/api/v1/repos/${codebergUser}/${repo.name}/commits?limit=1`);
                    if (cbCommitRes.ok) {
                        const count = cbCommitRes.headers.get('x-total-count');
                        if (count) stats.totalCommits += parseInt(count, 10);
                    }
                } catch(e) { console.warn('Could not fetch commits for', repo.name); }
            }
        }

        // 4. Update the UI with basic stats
        document.getElementById('git-total-repos').textContent = `${stats.publicRepos} Public Repositories`;
        document.getElementById('git-total-commits').textContent = `${stats.totalCommits}+ Commits (GH + CB)`;
        
        const starsEl = document.getElementById('git-total-stars');
        if (starsEl) starsEl.textContent = `${stats.stars} Stars`;

        const lastRepoEl = document.getElementById('git-latest-commit');
        if (stats.lastRepo) {
            let commitMsg = "Updated repository";
            try {
                if (stats.lastRepo.source === 'GitHub') {
                    const commitRes = await fetch(`https://api.github.com/repos/${githubUser}/${stats.lastRepo.name}/commits?per_page=1`);
                    if (commitRes.ok) {
                        const commits = await commitRes.json();
                        if (commits.length > 0) commitMsg = commits[0].commit.message.split('\n')[0];
                    }
                } else if (stats.lastRepo.source === 'Codeberg') {
                    const commitRes = await fetch(`https://codeberg.org/api/v1/repos/${codebergUser}/${stats.lastRepo.name}/commits?limit=1`);
                    if (commitRes.ok) {
                        const commits = await commitRes.json();
                        if (commits.length > 0) commitMsg = commits[0].commit.message.split('\n')[0];
                    }
                }
            } catch (e) { console.warn('Could not fetch last commit message'); }

            lastRepoEl.innerHTML = `<span class="repo-badge">[${stats.lastRepo.source}]</span> <a href="${stats.lastRepo.html_url}" target="_blank" style="color: inherit; text-decoration: underline;"><strong>${stats.lastRepo.name}</strong></a><br><code style="font-size: 0.85em; background: rgba(0,0,0,0.1); padding: 2px 4px; border-radius: 4px; display: inline-block; margin-top: 5px;">${commitMsg}</code> <span style="font-size: 0.8em; opacity: 0.8;">(${stats.lastRepo.updated.toLocaleDateString()})</span>`;
        }

        // 5. Build the Monthly Commits Chart using GitHub Events API
        const eventsRes = await fetch(`https://api.github.com/users/${githubUser}/events?per_page=100`);
        if (eventsRes.ok) {
            const events = await eventsRes.json();
            const monthlyCommits = {};
            
            // Group PushEvents by month
            events.forEach(ev => {
                if (ev.type === 'PushEvent' && ev.payload && ev.payload.commits) {
                    const date = new Date(ev.created_at);
                    const month = date.toLocaleString('default', { month: 'short' }) + ' ' + date.getFullYear().toString().slice(-2);
                    monthlyCommits[month] = (monthlyCommits[month] || 0) + ev.payload.commits.length;
                }
            });

            const chartContainer = document.getElementById('git-chart-container');
            if (chartContainer && Object.keys(monthlyCommits).length > 0) {
                const maxCommits = Math.max(...Object.values(monthlyCommits), 1);
                
                // Keep order chronological
                const monthsOrdered = Object.keys(monthlyCommits).reverse();

                let chartHTML = `<div style="display: flex; align-items: flex-end; justify-content: space-around; height: 120px; margin-top: 15px; padding-bottom: 5px; border-bottom: 1px solid rgba(255,255,255,0.2);">`;
                
                monthsOrdered.forEach(month => {
                    const count = monthlyCommits[month];
                    const heightPct = (count / maxCommits) * 100;
                    chartHTML += `
                        <div style="display: flex; flex-direction: column; align-items: center; width: 40px; position: relative;">
                            <div title="${count} commits" style="height: ${heightPct}px; width: 100%; background-color: var(--primary-color, #4CAF50); border-radius: 4px 4px 0 0; min-height: 4px; transition: height 0.3s; cursor: pointer;"></div>
                            <span style="font-size: 0.75rem; margin-top: 8px; opacity: 0.8; white-space: nowrap;">${month}</span>
                            <span style="position: absolute; top: -20px; font-size: 0.75rem; font-weight: bold;">${count}</span>
                        </div>
                    `;
                });
                
                chartHTML += `</div><p style="text-align:center; font-size: 0.85rem; margin-top: 15px; opacity: 0.7;">Recent Commits per Month (GitHub)</p>`;
                chartContainer.innerHTML = chartHTML;
            } else if (chartContainer) {
                chartContainer.innerHTML = '<p style="text-align:center; opacity:0.7;">No recent commit data available for chart.</p>';
            }
        }

    } catch (error) {
        console.error("Error fetching git stats:", error);
    }
});
