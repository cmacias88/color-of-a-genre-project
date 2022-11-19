const Link = ReactRouterDOM.Link;

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
            <NavBar />
            <ReactRouterDOM.Route exact path="/">
              <Homepage />
            </ReactRouterDOM.Route>
            <ReactRouterDOM.Route exact path="/signup">
                <SignUp />
            </ReactRouterDOM.Route>
            <ReactRouterDOM.Route exact path="/login">
                <Login />
            </ReactRouterDOM.Route>
        </ReactRouterDOM.BrowserRouter>
      );
}

ReactDOM.render(<App />, document.querySelector('#root'));