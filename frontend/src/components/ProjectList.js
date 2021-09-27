import { Link } from "react-router-dom";


const ProjectItem = ({ item, deleteProject }) => {
    return (
        <tr>
            <td><Link to={ `/projects/${item.id}/` } >{ item.name }</Link></td>
            <td>{ item.created }</td>
            <td>{ item.repo_url }</td>
            <td>{ item.users.join(', ') }</td>
            <td><button onClick={() => deleteProject(item.id)}>Delete</button></td>
        </tr>
    )
}


const ProjectList = ({ projects, deleteProject, standAlone }) => {
    return (
        projects.length
        ? <table>
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Created</th>
                    <th>Repo URL</th>
                    <th>Involved</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                { projects.map( project => <ProjectItem key={ project.id } item={ project } deleteProject={ deleteProject }/> ) }
            </tbody>
            { standAlone
                ? <tfoot>
                    <tr>
                        <td  colSpan="2"><Link to="/projects/search/">Search projects</Link></td>
                        <td  colSpan="2"><Link to="/projects/add/">Add new project</Link></td>
                    </tr>
                </tfoot>
                : null
            }
        </table>
        : <h2>no data</h2>
    )
}

export default ProjectList;
