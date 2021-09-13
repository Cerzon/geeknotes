import './App.css';
import React from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import UserList from './components/UserList';
import ProjectList from './components/ProjectList';
import ProjectDetail from './components/ProjectDetail';
import NoteList from './components/NoteList';
import LoginForm from './components/LoginForm';
import Logout from './components/Logout';
import Menu from './components/Menu';
import Footer from './components/Footer';
import { get, post } from './utils/reqs';


const pageNotFound = ({ location }) => {
    return (
        <div>
            <h1>The page at the url '{ location.pathname }' was not found</h1>
        </div>
    )
}


const userMenu = [
    {href: '/', name: 'Users'},
    {href: '/projects/', name: 'Projects'},
    {href: '/notes/', name: 'Notes'},
    {href: '/logout/', name: 'Logout'}
]

const anonMenu = [
    {href: '/login/', name: 'Login'}
]


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            users: [],
            projects: [],
            notes: [],
            token: "",
            is_authenticated: false
        };
        this.getToken = this.getToken.bind(this);
        this.removeToken = this.removeToken.bind(this);
    }

    componentDidMount() {
        this.getStoredToken();
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.is_authenticated !== prevState.is_authenticated && this.state.is_authenticated) {
            this.loadData();
        }
    }

    loadData() {
        const auth_header = this.getAuthHeader();
        Object.entries({
            users: 'users/',
            projects: 'projects/',
            notes: 'notes/'
        }).forEach(
            ([key, value]) =>  get(value, auth_header)
                                .then( data => this.setState({[key]: data.results}) )
                                .catch( err => console.log(err) )
        );
    }

    getAuthHeader() {
        return {Authorization: `Token ${ this.state.token }`}
    }

    getStoredToken() {
        const username = localStorage.getItem('username');
        const token = localStorage.getItem('token');
        if (username && token) {
            this.setState({token: token, is_authenticated: true});
        }
    }

    getToken(username, password) {
        post('token-auth/', {username, password})
        .then( data => this.setToken(username, data.token) )
        .catch( err => console.log(err) );
    }

    setToken(username, token) {
        this.setState({token: token, is_authenticated: true});
        localStorage.setItem('username', username);
        localStorage.setItem('token', token);
    }

    removeToken() {
        this.setState({token: '', is_authenticated: false});
        localStorage.removeItem('username');
        localStorage.removeItem('token');
    }

    render() {
        return (
            <div className="App">
                <BrowserRouter>
                    <Menu links={ this.state.is_authenticated ? userMenu : anonMenu }/>
                    <Switch>
                        <Route
                            exact path='/'
                            component={ () => <UserList users={ this.state.users }/> }
                        />
                        <Route
                            exact path='/projects/'
                            component={ () => <ProjectList projects={ this.state.projects }/> }
                        />
                        <Route
                            exact path='/projects/:id'
                            component={ location => <ProjectDetail project={ this.state.projects.find( el => el.id === parseInt(location.match.params.id) ) }/> }
                        />
                        <Route
                            exact path='/notes/'
                            component={ () => <NoteList notes={ this.state.notes } projects={ this.state.projects }/> }
                        />
                        <Route
                            exact path='/login/'
                            component={ () => <LoginForm getToken={ this.getToken } is_authenticated={ this.state.is_authenticated }/> }
                        />
                        <Route
                            exact path='/logout/'
                            component={ () => <Logout removeToken={ this.removeToken } is_authenticated={ this.state.is_authenticated }/> }
                        />
                        <Redirect from='/users/' to='/'/>
                        <Route component={ pageNotFound } />
                    </Switch>
                    <Footer/>
                </BrowserRouter>
            </div>
        )
    }
}

export default App;
