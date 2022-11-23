const Link = ReactRouterDOM.Link;
const Route = ReactRouterDOM.Route;


function NavBar () {
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


function Homepage() {
    return (
    <React.Fragment>
    <h1>Welcome!</h1>

    <p>
        Become a user and link your Spotify account to see a visualization of:
            <li>the percentage of genres in a playlist of your choosing</li>
	        <li>the most common colors of albums in those given genres</li>
    </p>

    <div>
        <li><Link to="/log-in">Already have an account? Log In Here</Link></li>
        <li><Link to="/sign-up">Want to save your visualizations? Sign Up Here</Link></li>
        <li><Link to="/playlist-selection">Or simply generate a visualization with a public playlist!</Link></li>
    </div>
    </React.Fragment>
    )
}


function Dashboard({user}) {
    return (
    <p>Welcome back {user.username}!</p>
    )
}


function UserSignUp({handleSubmit, setUser}) {
    return(
    <React.Fragment>
        <form id="sign-up" onSubmit={handleSubmit}>
        <h1>Sign Up</h1>
            <div>
                <label>First Name</label>
                    <input type="text" onChange={(evt) => setUser({ ...user, fname: evt.target.value })}/>
            </div>
            <div>
                <label>Last Name</label>
                    <input type="text" onChange={(evt) => setUser({ ...user, lname: evt.target.value })}/>
            </div>
            <div>
                <label>Username</label>
                    <input type="text" onChange={(evt) => setUser({ ...user, username: evt.target.value })}/>
            </div>
            <div>
                <label>Password</label>
                    <input type="password" onChange={(evt) => setUser({ ...user, password: evt.target.value })}/>
            </div>
            <div>
                <input type="submit" value="Sign Up"/>
            </div>
        </form>
        <p>
            <Link to="/log-in">Already registered?</Link>
        </p>
    </React.Fragment>
    )
};


function UserLogIn({handleSubmit, setUsername, setPassword}) {
    return(
    <React.Fragment>
        <form id="log-in" onSubmit={handleSubmit}>
        <h1>Log In</h1>
            <div>
                <label>Username</label>
                    <input type="text" id="username" onChange={(evt) => setUsername({ ...user, username: evt.target.value })}/>
            </div>
            <div>
                <label>Password</label>
                    <input type="password" id="password" onChange={(evt) => setPassword({ ...user, password: evt.target.value })}/>
            </div>
            <div>
                <input type="submit" value="Log In"/>
            </div>
        </form>
        <p>
            <Link to="/sign-up">Don't have an account?</Link>
        </p>
    </React.Fragment>
    )
};

function PlaylistInput({handleSubmit, setPlaylist}) {
    return(
        <React.Fragment>
            <form id="playlist-input" onSubmit={handleSubmit}>
            <h1>Provide a Playlist</h1>
                <div>
                    <label>Username</label>
                        <input type="text" id="playlist-link" onChange={(evt) => setPlaylist({ ...playlist, playlist_link: evt.target.value })}/>
                </div>
            </form>
        </React.Fragment>

    )
};


function App() {

    const [loggedIn, setLoggedIn] = React.useState(false)

    const [user, setUser] = React.useState({fname: "",
                                            lname: "",
                                            username: "",
                                            password: "" });

    const [playlist, setPlaylist] = React.useState({playlist_link: ""});


    const handleSignUpSubmit = (evt) => {
        evt.preventDefault();
        fetch('/api/sign-up', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(user)
            })
        .then((response) => response.json())
        .then((user_info) => {if (user_info.username) {
            setLoggedIn(true);
            };
        });
    };


    const handleLogInSubmit = (evt) => {
        evt.preventDefault();
        fetch('/api/log-in', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(user)
            })
        .then((response) => response.json())
        .then((user_info) => {if (user_info.username) {
            setUser({fname: user_info.fname,
                    lname: user_info.lname,
                    username: user_info.username,
                    password: user_info.password})
            setLoggedIn(true);
            };
        });
    };

    const handlePlaylistSubmit = (evt) => {
        evt.preventDefault();
        fetch('/api/playlist-selection', { 
            method: 'POST',
            headers: { 'Content-Type': 'application/json'},
            body: JSON.stringify(playlist)
            })
        .then((response) => response.json())
        .then((playlist) => {if (playlist.playlist_link) {
            setPlaylist({playlist_uri : playlist.playlist_link})
            };
        });
    };


    return (
        <ReactRouterDOM.BrowserRouter>
            <NavBar />
                <ReactRouterDOM.Route exact path="/">
                    <Homepage />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/sign-up">
                    <UserSignUp handleSubmit={handleSignUpSubmit} />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/log-in">
                    <UserLogIn handleSubmit={handleLogInSubmit} />
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/user-profile">
                    {/* <UserProfile /> */}
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/playlist-selection">
                    <PlaylistInput handleSubmit={handlePlaylistSubmit}/>
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/visualization-generator">
                    {/* <VisualizationGenerator /> */}
                </ReactRouterDOM.Route>
                <ReactRouterDOM.Route exact path="/spotify-authorization">
                    {/* <SpotifyAuth /> */}
                </ReactRouterDOM.Route>
        </ReactRouterDOM.BrowserRouter>
    );
}


ReactDOM.render(<App />, document.querySelector('#root'));