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
    <p>
        Become a user and link your Spotify account to see a visualization of:
            <li>the percentage of genres in a playlist of your choosing</li>
	        <li>the most common colors of albums in those given genres</li>
    </p>
    <li><Link to="/log-in">Already have an account? Log In Here</Link></li>
    <li><Link to="/sign-up">Want to save your visualizations? Sign Up Here</Link></li>
    <li><Link to="/playlist-selection">Or simply generate a visualization with a public playlist!</Link></li>
    </React.Fragment>
    )
}


function Welcome(props) {
    return (
    <p>Welcome {props.username}!</p>
    )
}


function SignUpButton() {
    return (
        <button type="button" onSubmit={SignUpForm}>
        Sign Up
        </button>
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
    return(
    <React.Fragment>
        <form>
        <h1>Sign Up</h1>
            <div>
                <label>First Name</label>
                    <input type="text"/>
            </div>
            <div>
                <label>Last Name</label>
                    <input type="text"/>
            </div>
            <div>
                <label>Username</label>
                    <input type="text"/>
            </div>
            <div>
                <label>Password</label>
                    <input type="password"/>
            </div>
            <div>
                <SignUpButton />
            </div>
            <p>
                Already registered? <a href="/log-in">Log In</a>
            </p>
        </form>
    </React.Fragment>
    )
};

function UserLogIn() {
    return(
    <React.Fragment>
        <form>
        <h1>Log In</h1>
            <div>
                <label>Username</label>
                    <input type="text"/>
            </div>
            <div>
                <label>Password</label>
                    <input type="password"/>
            </div>
            <div>
                <LogInButton />
            </div>
            <p>
                Don't have an account? <a href="/sign-up">Sign Up</a>
            </p>
        </form>
    </React.Fragment>
    )
};


function App() {
    return (
        <ReactRouterDOM.BrowserRouter>
            <Navbar />
                <ReactRouterDOM.Route exact path="/">
                    <Homepage />
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