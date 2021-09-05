import './App.css';
import React from 'react';
import { BrowserRouter, Switch, Route, Redirect } from 'react-router-dom';
import UserList from './components/UserList';
import ProjectList from './components/ProjectList';
import ProjectDetail from './components/ProjectDetail';
import NoteList from './components/NoteList';
import Menu from './components/Menu';
import Footer from './components/Footer';
import { get } from './utils/reqs';


const pageNotFound = ({ location }) => {
    return (
        <div>
            <h1>The page at the url '{ location.pathname }' was not found</h1>
        </div>
    )
}


const menuLinks = [
    { href: '/', name: 'Users' },
    { href: '/projects/', name: 'Projects' },
    { href: '/notes/', name: 'Notes' }
]


class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            users: [],
            projects: [],
            notes: []
        };
    }

    componentDidMount() {
        get('users/').then( data => this.setState({ users: data.results }));
        get('projects/').then( data => this.setState({ projects: data.results }));
        get('notes/').then( data => this.setState({ notes: data.results }));
    }

    render() {
        return (
            <div className="App">
                <BrowserRouter>
                    <Menu links={ menuLinks }/>
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
