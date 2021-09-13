import React from "react";
import { Redirect } from "react-router-dom";


export default class LoginForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            username: "",
            password: ""
        };
        this.handleFieldChange = this.handleFieldChange.bind(this);
        this.handleFormSubmit = this.handleFormSubmit.bind(this);
    }

    handleFieldChange(event) {
        this.setState({ [event.target.name]: event.target.value })
    }

    handleFormSubmit(event) {
        event.preventDefault();
        this.props.getToken(this.state.username, this.state.password);
    }

    render() {
        return (
            this.props.is_authenticated
            ? <Redirect push to='/' />
            : <form onSubmit={ this.handleFormSubmit }>
                <p>
                    <label>Username</label>
                    <input
                        type="text"
                        name="username"
                        onChange={ this.handleFieldChange }
                    />
                </p>
                <p>
                    <label>Password</label>
                    <input
                        type="password"
                        name="password"
                        onChange={ this.handleFieldChange }
                    />
                </p>
                <p>
                    <input type="submit" value="Login"/>
                </p>
            </form>
        )
    }
}
