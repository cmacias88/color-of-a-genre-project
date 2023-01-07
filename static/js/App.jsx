function App() {

    let [user, setUser] = React.useState({id: Number(localStorage.getItem("userId")),
                                            fname: localStorage.getItem("userFname"),
                                            lname: localStorage.getItem("userLname"),
                                            username: localStorage.getItem("userUsername"),
                                            password: localStorage.getItem("userPassword")});

    let [loggedIn, setLoggedIn] = React.useState(JSON.parse(localStorage.getItem("isLoggedIn")));

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

    return (
        <ReactRouterDOM.BrowserRouter>
                <NavBar loggedIn={loggedIn} handleLogout={handleLogout}/>
                    <ReactRouterDOM.Route exact path="/">
                        <Homepage />
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/sign-up">
                        <UserSignUp />
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/my-profile">
                        <UserVisualizations />
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/log-in">
                        {loggedIn ? <ReactRouterDOM.Redirect to={"/my-profile/"} />:
                        <UserLogIn handleLogIn={handleLogIn}
                        setUsername={(evt) => setUser({ ...user, username: evt.target.value })}
                        setPassword={(evt) => setUser({ ...user, password: evt.target.value })} />}
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route exact path="/playlist-selection">
                        <PlaylistInput/>
                    </ReactRouterDOM.Route>
                    <ReactRouterDOM.Route path={`/visualization-generator/${playlist.playlist_id}`}>
                        <VisualizationGenerator />
                    </ReactRouterDOM.Route> 
        </ReactRouterDOM.BrowserRouter>
    );
}

ReactDOM.render(<App />, document.querySelector('#root'));