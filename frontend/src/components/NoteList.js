import { Link } from "react-router-dom";
import { Active, Closed } from "../static/Icons";


const NoteAuthor = ({ author }) => {
    return (
        <td>
            <p>{ author.first_name } { author.last_name }</p>
            <p>{ author.email }</p>
        </td>
    )
}


const NoteItem = ({ item, project, deleteNote }) => {
    return (
        <tr>
            <td><Link to={ `/projects/${item.project}/` } >{ project.name }</Link></td>
            <NoteAuthor author={ item.author } />
            <td>{ item.created }</td>
            <td>{ item.updated }</td>
            <td>{ item.is_active ? <Active/> : <Closed/> }</td>
            <td>{ item.body }</td>
            <td><button onClick={() => deleteNote(item.id)}>Delete</button></td>
        </tr>
    )
}


const NoteList = ({ notes, projects, deleteNote }) => {
    return (
        notes.length
        ? <table>
            <thead>
                <tr>
                    <th>Project</th>
                    <th>Author</th>
                    <th>Created</th>
                    <th>Updated</th>
                    <th>Is Active</th>
                    <th>Text</th>
                    <th></th>
                </tr>
            </thead>
            <tbody>
                {
                    notes.map( note => <NoteItem 
                        key={ note.id }
                        item={ note }
                        project={ projects.find( el => el.id === note.project ) }
                        deleteNote={ deleteNote }
                    /> ) 
                }
            </tbody>
            <tfoot>
                <tr>
                    <td colSpan="7"><Link to="/notes/add/">Add new note</Link></td>
                </tr>
            </tfoot>
        </table>
        : <h2>no data</h2>
    )
}

export default NoteList;
