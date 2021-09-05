const ProjectDetail = ({ project }) => {
    return (
        <table>
            <tbody>
                <tr>
                    <th>Name:</th>
                    <td>{ project.name }</td>
                </tr>
                <tr>
                    <th>Created:</th>
                    <td>{ project.created }</td>
                </tr>
                <tr>
                    <th>Repo URL:</th>
                    <td>{ project.repo_url }</td>
                </tr>
                <tr>
                    <th>Involved Users:</th>
                    <td>{ project.users.join(', ') }</td>
                </tr>
            </tbody>
        </table>
    )
}


export default ProjectDetail;
