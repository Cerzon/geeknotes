import { Link } from "react-router-dom";


const ProjectItem = ({ item }) => {
    return (
        <tr>
            <td><Link to={ `/projects/${item.id}/` } >{ item.name }</Link></td>
            <td>{ item.created }</td>
            <td>{ item.repo_url }</td>
            <td>{ item.users.join(', ') }</td>
        </tr>
    )
}


const ProjectList = ({ projects }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Created</th>
                    <th>Repo URL</th>
                    <th>Involved</th>
                </tr>
            </thead>
            <tbody>
                { projects.map( project => <ProjectItem key={ project.id } item={ project }/> ) }
            </tbody>
        </table>
    )
}

export default ProjectList;
