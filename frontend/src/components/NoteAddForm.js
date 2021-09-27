import React from "react";


export default class ProjectAddForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            noteProject: '',
            noteAuthor: '',
            noteBody: ''
        }
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleSelectChange = this.handleSelectChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
    }

    handleFieldChange(event) {
        this.setState({[event.target.name]: event.target.value});
    }

    handleSelectChange(event) {
        this.setState({[event.target.name]: parseInt(event.target.value)});
    }

    handleFormSubmit(event) {
        event.preventDefault();
        this.props.addNewNote(this.state.noteProject, this.state.noteAuthor, this.state.noteBody);
    }

    render() {
        return (
            <form onSubmit={ this.handleFormSubmit }>
                <p>
                    <label>Project</label>
                    <select name="noteProject" onChange={ this.handleSelectChange } required>
                        { this.props.projects.map(
                            project => <option value={ project.id } key={ project.id }>
                                        { project.name }
                                    </option>
                        ) }
                    </select>
                </p>
                <p>
                    <label>Author</label>
                    <select name="noteAuthor" onChange={ this.handleSelectChange } required>
                        { this.props.users.map(
                            user => <option value={ user.id } key={ user.id }>
                                        { user.first_name && user.last_name
                                        ? `${ user.first_name } ${ user.last_name }`
                                        : user.username }
                                    </option>
                        ) }
                    </select>
                </p>
                <p>
                    <label>Text</label>
                    <textarea name="noteBody" onChange={ this.handleFieldChange }></textarea>
                </p>
                <p>
                    <input type="submit" value="Create" />
                </p>
            </form>
        )
    }
}
