import './App.css';
import React from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import UserList from './components/UserList';
import ProjectList from './components/ProjectList';
import ProjectDetail from './components/ProjectDetail';
import ProjectAddForm from './components/ProjectAddForm';
import ProjectsSearchForm from './components/ProjectsSearchForm';
import NoteList from './components/NoteList';
import NoteAddForm from './components/NoteAddForm';
import LoginForm from './components/LoginForm';
import Logout from './components/Logout';
import Menu from './components/Menu';
import Footer from './components/Footer';
import { get, post, del } from './utils/reqs';


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

const apiUsers = {users: 'users/'}
const apiProjects = {projects: 'projects/'}
const apiNotes = {notes: 'notes/'}


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            users: [],
            projects: [],
            notes: [],
            foundProjects: null,
            token: "",
            is_authenticated: false
        };
        this.getToken = this.getToken.bind(this);
        this.removeToken = this.removeToken.bind(this);
        this.addNewProject = this.addNewProject.bind(this);
        this.deleteProject = this.deleteProject.bind(this);
        this.addNewNote = this.addNewNote.bind(this);
        this.deleteNote = this.deleteNote.bind(this);
        this.getFilteredProjects = this.getFilteredProjects.bind(this);
    }

    componentDidMount() {
        this.getStoredToken();
    }

    componentDidUpdate(prevProps, prevState) {
        if (this.state.is_authenticated !== prevState.is_authenticated && this.state.is_authenticated) {
            this.loadData(Object.assign({}, apiUsers, apiProjects, apiNotes));
        }
    }

    loadData(sources) {
        const authHeader = this.getAuthHeader();
        Object.entries(sources).forEach(
            ([key, value]) =>  get(value, authHeader)
                                .then(data => this.setState({[key]: data.results}))
                                .catch(err => console.log(err))
        );
    }

    addNewProject(projectName, repoUrl, involvedUsers) {
        const authHeader = this.getAuthHeader();
        const data = {
            name: projectName,
            repo_url: repoUrl,
            users: involvedUsers
        };
        post('projects/', data, authHeader)
        .then(newItem => {
            get(`projects/${newItem.id}`, authHeader)
            .then(project => this.setState({projects: [...this.state.projects, project]}))
            .catch(err => console.log(err))
        })
        .catch(err => console.log(err))
    }

    addNewNote(noteProject, noteAuthor, noteBody) {
        const authHeader = this.getAuthHeader();
        const data = {
            project: noteProject,
            author: noteAuthor,
            body: noteBody
        };
        post('notes/', data, authHeader)
        .then(newItem => {
            get(`notes/${newItem.id}`, authHeader)
            .then(note => this.setState({notes: [...this.state.notes, note]}))
            .catch(err => console.log(err))
        })
        .catch(err => console.log(err))
    }

    deleteProject(id) {
        const authHeader = this.getAuthHeader();
        del(`projects/${id}/`, authHeader)
        .then(response => {
            if (response.ok && response.status === 204) {
                this.setState({
                    projects: this.state.projects.filter(item => item.id !== id)
                });
                // this.loadData(apiProjects);
            }
        })
        .catch(err => console.log(err));
    }

    deleteNote(id) {
        const authHeader = this.getAuthHeader();
        del(`notes/${id}/`, authHeader)
        .then(response => {
            if (response.ok && response.status === 204) {
                this.setState({
                    notes: this.state.notes.filter(item => item.id !== id)
                });
                // this.loadData(apiNotes);
            }
        })
        .catch(err => console.log(err));
    }

    getFilteredProjects(searchText) {
        const authHeader = this.getAuthHeader();
        const urlParams = {name: searchText};
        get('projects/', authHeader, urlParams)
        .then(data => this.setState({foundProjects: data.results}))
        .catch(err => console.log(err));
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
        .then(data => this.setToken(username, data.token))
        .catch(err => console.log(err));
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
                            component={() => <UserList users={ this.state.users }/>}
                        />
                        <Route
                            exact path='/projects/'
                            component={() => <ProjectList projects={ this.state.projects } deleteProject={ this.deleteProject } standAlone={ true }/>}
                        />
                        <Route exact path='/projects/search/'>
                            <ProjectsSearchForm getFilteredProjects={ this.getFilteredProjects }>
                                {
                                    this.state.foundProjects
                                    ? <ProjectList projects={ this.state.foundProjects } deleteProject={ this.deleteProject }/>
                                    : null
                                }
                            </ProjectsSearchForm>
                        </Route>
                        <Route
                            exact path='/projects/add/'
                            component={() => <ProjectAddForm users={ this.state.users } addNewProject={ this.addNewProject }/>}
                        />
                        <Route
                            exact path='/projects/:id'
                            component={({match}) => <ProjectDetail project={ this.state.projects.find(el => el.id === parseInt(match.params.id)) }/>}
                        />
                        <Route
                            exact path='/notes/add/'
                            component={() => <NoteAddForm projects={ this.state.projects } users={ this.state.users } addNewNote={ this.addNewNote }/>}
                        />
                        <Route
                            exact path='/notes/'
                            component={() => <NoteList notes={ this.state.notes } projects={ this.state.projects } deleteNote={ this.deleteNote }/>}
                        />
                        <Route
                            exact path='/login/'
                            component={() => <LoginForm getToken={ this.getToken } is_authenticated={ this.state.is_authenticated }/>}
                        />
                        <Route
                            exact path='/logout/'
                            component={() => <Logout removeToken={ this.removeToken } is_authenticated={ this.state.is_authenticated }/>}
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
