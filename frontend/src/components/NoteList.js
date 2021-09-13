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


const NoteItem = ({ item, project }) => {
    return (
        <tr>
            <td><Link to={ `/projects/${item.project}/` } >{ project.name }</Link></td>
            <NoteAuthor author={ item.author } />
            <td>{ item.created }</td>
            <td>{ item.updated }</td>
            <td>{ item.is_active ? <Active/> : <Closed/> }</td>
            <td>{ item.body }</td>
        </tr>
    )
}


const NoteList = ({ notes, projects }) => {
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
                </tr>
            </thead>
            <tbody>
                {
                    notes.map( note => <NoteItem 
                        key={ note.id }
                        item={ note }
                        project={ projects.find( el => el.id === note.project ) }
                    /> ) 
                }
            </tbody>
        </table>
        : <h2>no data</h2>
    )
}

export default NoteList;
