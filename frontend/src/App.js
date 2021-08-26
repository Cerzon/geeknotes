import './App.css';
import React from 'react';
import UserList from './components/Users';
import Menu from './components/Menu';
import Footer from './components/Footer';
import { get } from './utils/reqs';


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = { users: [] };
    }

    componentDidMount() {
        get('users/').then( users => this.setState({ users }));
    }

    render() {
        return (
            <div className="App">
                <Menu/>
                <UserList users={ this.state.users }/>
                <Footer/>
            </div>
        )
    }
}

export default App;
