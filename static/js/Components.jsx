function NavBar ({loggedIn, handleLogout}) {

    if (loggedIn){
        return (
            <nav>
                <section>
                    <ReactRouterDOM.NavLink 
                        to="/" 
                        activeClassName="nav-active" 
                        className="navbar"
                        >
                        Home  
                    </ReactRouterDOM.NavLink>
                    <ReactRouterDOM.NavLink 
                        to="/my-profile" 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        My Profile
                    </ReactRouterDOM.NavLink>
                    <ReactRouterDOM.NavLink 
                        to="/playlist-selection" 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        Visualization Generator
                    </ReactRouterDOM.NavLink>
                    <ReactRouterDOM.NavLink 
                        to="/" 
                        onClick={handleLogout} 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        Logout  
                    </ReactRouterDOM.NavLink>
                    <ReactRouterDOM.NavLink 
                        to="/browse-visualizations" 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        Browse Visualizations
                    </ReactRouterDOM.NavLink>
                </section>
            </nav>
        );
    } else {
        return (
            <nav>
                <section>
                    <ReactRouterDOM.NavLink 
                        to="/" 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        Home
                    </ReactRouterDOM.NavLink>
                    <ReactRouterDOM.NavLink 
                        to="/playlist-selection" 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        Visualization Generator
                    </ReactRouterDOM.NavLink>
                    <ReactRouterDOM.NavLink 
                        to="/browse-visualizations" 
                        activeClassName="nav-active" 
                        className="navbar"
                    >
                        Browse Visualizations
                    </ReactRouterDOM.NavLink>
                </section>
            </nav>
        );
    }
}


function Homepage() {
    return(
    <React.Fragment>
        <h1>Welcome!</h1>

        <p>
            Become a user and link your Spotify account to see a visualization of:
                <li>the percentage of genres in a playlist of your choosing</li>
                <li>the most common colors of albums in those given genres</li>
        </p>

        <div>
            <ReactRouterDOM.Link to="/log-in">Already have an account? Log In Here</ReactRouterDOM.Link>
        </div>
        <div>
            <ReactRouterDOM.Link to="/sign-up">Want to save your visualizations? Sign Up Here</ReactRouterDOM.Link>
        </div>
        <div>
            <ReactRouterDOM.Link to="/playlist-selection">Or simply generate a visualization with a public playlist!</ReactRouterDOM.Link>
        </div>
    </React.Fragment>
    )
}


function UserLogIn({handleLogIn, setUsername, setPassword}) {
    
    const [data, setData] = React.useState({
        password: "",
        showPassword: false,
    });

    return(
        <React.Fragment>
            <form id="log-in" onSubmit={handleLogIn}>
                <h1>
                    Log In
                </h1>
                <div>
                    <label>
                        Username
                        <input type="text" 
                                id="username"
                                name="username" 
                                onChange={setUsername}/>
                    </label>
                </div>
                <div>
                    <label>
                        Password
                        <input type={data.showPassword ? "text" : "password"} 
                                id="password" 
                                name="password" 
                                onChange={setPassword}/>
                    </label>
                </div>
                <div>
                    <input type="submit" value="Log In"/>
                </div>
            </form>
            <p>
                <ReactRouterDOM.Link to="/sign-up">Don't have an account?</ReactRouterDOM.Link>
            </p>
    </React.Fragment>
    )
};


function UserSignUp() {

    const [fname, setFname] = React.useState("");
    const [lname, setLname] = React.useState("");
    const [username, setUsername] = React.useState("");
    const [password, setPassword] = React.useState("");

    const [data, setData] = React.useState({
        password: "",
        showPassword: false,
    });

    const handleSubmit = async (evt) => {
        evt.preventDefault();
        let newUser = await fetch('/sign-up', { 
            method: "POST",
            headers: { 
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
            body: JSON.stringify({
                fname: fname,
                lname: lname,
                username: username,
                password: password,
                }),
            });

        if(newUser.status===200){
            alert("You have successfully made an account.");
    
        } else if (newUser.status===401) {
            alert("An account already exists with that username. Please try again.");
            location.reload();
        }
    };


    return(
        <React.Fragment>
            <form id="sign-up" onSubmit={handleSubmit}>
                <h1>
                    Sign Up
                </h1>
                <div>
                    <label>
                        First Name
                        <input type="text" 
                                id="fname"
                                name="fname"
                                onChange={(evt) => setFname(evt.target.value)}/>
                    </label>
                </div>
                <div>
                    <label>
                        Last Name
                        <input type="text" 
                                id="lname"
                                name="lname"
                                onChange={(evt) => setLname(evt.target.value)}/>
                    </label>
                </div>
                <div>
                    <label>
                        Username
                        <input type="text" 
                                id="username"
                                name="username"
                                onChange={(evt) => setUsername(evt.target.value)}/>
                    </label>
                </div>
                <div>
                    <label>
                        Password
                        <input type={data.showPassword ? "text" : "password"} 
                                id="password" 
                                name="password" 
                                onChange={(evt) => setPassword(evt.target.value)}/>
                    </label>
                </div>
                <div>
                    <input type="submit" value="Sign Up"/>
                </div>
            </form>
        <p>
            <ReactRouterDOM.Link to="/log-in">Already registered?</ReactRouterDOM.Link>
        </p>
    </React.Fragment>
    )
};


function SuccessfulSignUpAlert() {
    return (
        <React.Fragment>
            <Alert onClose={() => { } }>This is a success alert — check it out!</Alert>
            <Alert action=
                        {<Button>
                            UNDO
                        </Button>}
            >
                This is a success alert — check it out!
            </Alert>
        </React.Fragment>
    )
}


function PlaylistInput({handlePlaylistSubmit}) {

    const [playlistLink, setPlaylistLink] = React.useState("");

    return(
        <React.Fragment>
            <form id="playlist-selection" onSubmit={handlePlaylistSubmit}>
                <h1>
                    Playlist Visualizer 
                </h1>
                <div>
                    <label>
                        Playlist URL
                        <input type="text" 
                                id="playlist_link"
                                name="playlist_link" 
                                onChange={(evt) => setPlaylistLink(evt.target.value)}/>
                    </label>
                </div>
                <div>
                    <input type="submit" value="Submit Playlist"/>
                </div>
            </form>
    </React.Fragment>
    )
};


function AllUserVisualizations() {

    const [userVisualizations, setUserVisualizations] = useState([]);
        
    const alluserVisualizations = async (evt) => {
        const loadingVisualizations = await fetch('/my-profile')
            .then((response) => response.json())
            .then((userVisualizations) => setUserVisualizations(userVisualizations))
        };

    useEffect(() => {
        alluserVisualizations();
    }, []);

    return (
        <React.Fragment>
            <h1>
                Your Visualizations
            </h1>
            <li>
                {userVisualizations.map(info => 
                    <ReactRouterDOM.Link key={info.playlist_id} to={`/visualization-data/${info.playlist_id}`}>{info.playlist_name} by {info.user_id}</ReactRouterDOM.Link>)}
            </li>
        </React.Fragment>
    );

};


function VisualizationGenerator() {

    return (
        <React.Fragment>
            <h1>
            Success.
            </h1>
        </React.Fragment>
    )

};

//     let newVisualization = fetch('/visualization-data/<playlist_id>')
//         .then(response => response.json())
//         .then(responseJson => {
//             const data = responseJson.data.map(
//                 data.genre, data.genre_percentage
//             );
//         });

            
//     const chartOptions = {
//         rotation: -90,
//         cutout: "45%",
//         plugins: {
//         title: {
//             display: true,
//             position: "bottom",
//             text: "Your Playlist's Genre Percentages",
//             font: {
//             size: 32
//             }
//         },
//         legend: {
//             position: "left",
//             align: "start"
//             }
//         },
//         animation: {
//             animateRotate: true,
//             animateScale: true
//         }
//     };

//     new Chart(document.querySelector('#visualization'), {
//         type: 'doughnut',
//         data: {
//         datasets: [{
//             label: 'Playlist Genres',
//             data, 
//             options: chartOptions
//             }],
//         },
//     });
// };
