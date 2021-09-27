import React from "react";


export default class ProjectAddForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            projectName: '',
            repoUrl: '',
            involvedUsers: []
        }
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleSelectChange = this.handleSelectChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
    }

    handleFieldChange(event) {
        this.setState({ [event.target.name]: event.target.value });
    }

    handleSelectChange(event) {
        this.setState(
            {involvedUsers: [...event.target.selectedOptions].map(item => parseInt(item.value))}
        );
    }

    handleFormSubmit(event) {
        event.preventDefault();
        this.props.addNewProject(this.state.projectName, this.state.repoUrl, this.state.involvedUsers);
    }

    render() {
        return (
            <form onSubmit={ this.handleFormSubmit }>
                <p>
                    <label>Name</label>
                    <input type="text" name="projectName" onChange={ this.handleFieldChange } required/>
                </p>
                <p>
                    <label>Repo URL</label>
                    <input type="url" name="repoUrl" onChange={ this.handleFieldChange }/>
                </p>
                <p>
                    <label>Involved users</label>
                    <select name="involvedUsers" multiple onChange={ this.handleSelectChange } required>
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
                    <input type="submit" value="Create" />
                </p>
            </form>
        )
    }
}
