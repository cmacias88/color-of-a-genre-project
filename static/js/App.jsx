const Link = ReactRouterDOM.Link;
const Route = ReactRouterDOM.Route;


function NavBar (props) {
    return (
        <nav>
            <ReactRouterDOM.Link to="/" className="navbar">
                <span>  Home  </span>
            </ReactRouterDOM.Link>
            <ReactRouterDOM.Link to="/user-profile" className="navbar">
                <span>  My Profile  </span>
            </ReactRouterDOM.Link>
            <ReactRouterDOM.Link to="/playlist-selection" className="navbar">
                <span>  Playlist Selection  </span>
            </ReactRouterDOM.Link>
            <ReactRouterDOM.Link to="/spotify-authorization" className="navbar">
                <span>  Spotify Authorization </span>
            </ReactRouterDOM.Link>
        </nav>
    )
}


function Homepage(props) {
    return (
    <React.Fragment>
    <h1>Welcome!</h1>
    
    <li><Link to="/log-in">Log In</Link></li>
    <li><Link to="/sign-up">Sign Up</Link></li>
    </React.Fragment>
    )
}


function Welcome(props) {
    return (
    <p>Welcome {props.username}!</p>
    )
}


function LogInButton() {
    return (
        <button type="button" onSubmit={LogInForm}>
        Log In
        </button>
    )
}


function UserSignUp() {
    return (
        <div className="form">
        <form>
            <input type="text" name="username"></input>
            <input type="password" name="password"></input>
            <input type="submit"></input>
        </form>
        </div>
    )
}


function UserLogin() {
    return (
        <div className="form">
        <form>
            <input type="text" name="username"></input>
            <input type="password" name="password"></input>
            <input type="submit"></input>
        </form>
        </div>
    )
}


function App() {
    return (
        <ReactRouterDOM.BrowserRouter>
            <Navbar />
                <ReactRouterDOM.Route exact path="/">
                    <Homepage />
                    <SearchBar />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/sign-up">
                    <UserSignUp />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/log-in">
                    <UserLogin />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/user-profile">
                    <UserProfile />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/playlist-selection">
                    <PlaylistSelction />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/visualization-generator">
                    <VisualizationGenerator />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/spotify-authorization">
                    <SpotifyAuth />
                </ReactRouterDOM.Route>
        </ReactRouterDOM.BrowserRouter>

    );
}


ReactDOM.render(<App />, document.querySelector('#root'));