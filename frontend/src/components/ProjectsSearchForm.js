import React from "react";


export default class ProjectsSearchForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {searchText: ''};
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
    }

    handleFieldChange(event) {
        this.setState({ [event.target.name]: event.target.value });
    }

    handleFormSubmit(event) {
        event.preventDefault();
        this.props.getFilteredProjects(this.state.searchText)
    }

    render() {
        return (
            <>
            <form onSubmit={ this.handleFormSubmit }>
                <p>
                    <label>Project name contains</label>
                    <input
                        type="text"
                        name="searchText"
                        onChange={ this.handleFieldChange }
                    />
                </p>
                <p>
                    <input type="submit" value="Find"/>
                </p>
            </form>
            { this.props.children }
            </>
        )
    }
}
