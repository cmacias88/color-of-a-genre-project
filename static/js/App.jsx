function App() {

    let [user, setUser] = React.useState({id: Number(localStorage.getItem("userId")),
                                            fname: localStorage.getItem("userFname"),
                                            lname: localStorage.getItem("userLname"),
                                            username: localStorage.getItem("userUsername"),
                                            password: localStorage.getItem("userPassword")});

    let [loggedIn, setLoggedIn] = React.useState(JSON.parse(localStorage.getItem("isLoggedIn")));

    // let [validPlaylist, setvalidPlaylist] = React.useState(JSON.parse(localStorage.getItem("isValidPlaylist")));

    let handleLogIn = async (evt) => {
        evt.preventDefault();

        let userExists = await fetch("/log-in", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                username: user.username,
                password: user.password
            }),
        });

        if(userExists.status===200){
            let foundUser = await fetch("/log-in", {
                method: "POST",
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    username: user.username,
                    password: user.password
                }),
            })
            .then((response) => response.json())
            .then((data) => setUser({id: data.id,
                                    fname: data.fname,
                                    lname: data.lname,
                                    username: data.username,
                                    password: data.password
            }));
            setLoggedIn(true);
            localStorage.setItem("isLoggedIn", true);

        } else if (userExists.status===401){
            alert(userExists.statusText);
        }
    };


    function setSession() {
        localStorage.setItem("userId", user.id);
        localStorage.setItem("userFname", user.fname);
        localStorage.setItem("userLname", user.lname);
        localStorage.setItem("userUsername", user.username);
        localStorage.setItem("userPassword", user.password);
    }

    Promise.all([handleLogIn, setSession()]);


    let handleLogout = async (evt) => {
        evt.preventDefault();
        setLoggedIn(false);
        localStorage.setItem("isLoggedIn", false);
        setUser({id: "",
                fname:"",
                lname:"",
                username:"",
                password:""});
        
        let removeUser = await fetch("/log-out", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
                },
            body: JSON.stringify({
                username: user.username
            }),
        });
    };


    React.useEffect(() => {
        const isLoggedIn = localStorage.getItem("isLoggedIn");
        if (isLoggedIn === 'true') {
            setLoggedIn(true);
        } else {
            setLoggedIn(false);
        }
    }, []);


    // const handlePlaylistSubmit = async (evt) => {
    //     evt.preventDefault();
    //     let newPlaylist = await fetch('/playlist-selection', { 
    //         method: "POST",
    //         headers: { 
    //             'Accept': 'application/json',
    //             'Content-Type': 'application/json'
    //             },
    //         body: JSON.stringify({
    //             playlist_name: playlist_name, 
    //             playlist_uri: playlist_uri, 
    //             tracks: tracks
    //             }),
    //         });

    //     if(newPlaylist.status===200){
    //         ;setvalidPlaylist(true);
    //         localStorage.setItem("isValidPlaylist", true);

    //     } else if (newPlaylist.status===401) {
    //         window.flash("The playlist URL you entered is not valid. Please try again.");
    //         location.reload();
    //     };
    // };

    // React.useEffect(() => {
    //     const isValidPlaylist = localStorage.getItem("isValidPlaylist");
    //     if (isValidPlaylist === 'true') {
    //         setvalidPlaylist(true);
    //     } else {
    //         setvalidPlaylist(false);
    //     }
    // }, []);

    return (
        <ReactRouterDOM.BrowserRouter>
                <NavBar loggedIn={loggedIn} handleLogout={handleLogout}/>
                    <ReactRouterDOM.Route exact path="/">
                        <Homepage />
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/sign-up">
                        {loggedIn ? <ReactRouterDOM.Redirect to={"/"} />:
                        <UserSignUp user={user}/>}
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/my-profile">
                        <AllUserVisualizations/>
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/log-in">
                        {loggedIn ? <ReactRouterDOM.Redirect to={"/"} />:
                        <UserLogIn handleLogIn={handleLogIn}
                        setUsername={(evt) => setUser({ ...user, username: evt.target.value })}
                        setPassword={(evt) => setUser({ ...user, password: evt.target.value })} />}
                    </ReactRouterDOM.Route>
                    {/* <ReactRouterDOM.Route exact path="/playlist-selection">
                        {validPlaylist ? <ReactRouterDOM.Redirect to={`/visualization-generator/${playlist.playlist_id}`} />:
                        <PlaylistInput handlePlaylistSubmit={handlePlaylistSubmit}/>}
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/visualization-generator/:playlist_id">
                        <VisualizationGenerator />
                    </ReactRouterDOM.Route>  */}
                    {/* <ReactRouterDOM.Route exact path="/browse-visualizations">
                        <AllVisualizations/>
                    </ReactRouterDOM.Route> */}
        </ReactRouterDOM.BrowserRouter>
    );
}

ReactDOM.render(<App />, document.querySelector('#root'));