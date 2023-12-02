import React, { useState } from "react";

import { useNavigate } from "react-router-dom";


export async function createSession(email, password, props) {
    let token = "";
    // fetch(
    //     "http://localhost:8000/v1/authn/user-sessions/",
    //     {
    //         method: "POST",
    //         headers: {
    //             "Content-Type": "application/json",
    //         },
    //         body: JSON.stringify({
    //             username: email,
    //             password: password,
    //         })
    //     }
    // ).then(r => {
    //     if (r.ok) {
    //         return r.json();
    //     } else {
    //         console.log(r)
    //         throw new Error("failed to login");
    //     }
    // }).then((data) => {
    //     token = data.token;
    // });
    const response = await fetch(
        "http://localhost:8000/v1/authn/user-sessions/",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: email,
                password: password,
            })
        }
    )

    if (!response.ok) {
        console.log(response);
        throw new Error("failed to login");
    }

    const data = await response.json();

    return data.token;
}

export async function deleteSession() {
    const userToken = JSON.parse(localStorage.getItem("user")).token;

    let loggedOut = false;

    fetch(
        "http://localhost:8000/v1/authn/user-sessions/",
        {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + userToken,
                "Content-Type": "application/json",
            },
        }
    ).then(r => {
        if(!r.ok) {
            console.log("unable to log out");
        } else {
            console.log("logged out successfully");
            loggedOut = true;
        }
    })

    if (!loggedOut) {
        throw new Error("unable to log out!");
    }
}


const Login = (props) => {

    const navigate = useNavigate();

    const {loggedIn} = props

    const [email, setEmail] = useState("")

    const [password, setPassword] = useState("")

    const [emailError, setEmailError] = useState("")

    const [passwordError, setPasswordError] = useState("")

    const onButtonClick = () => {
        setEmailError("");
        setPasswordError("");

        if("" === email) {
            setEmailError("Please enter your email");
            return
        }

        if (!/^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$/.test(email)) {
            setEmailError("Please enter a valid email")
            return
        }

        if ("" === password) {
            setPasswordError("Please enter your password")
            return
        }

        if (password.length < 7) {
            setPasswordError("password must be atleast 8 characters");
            return
        }

        if (!loggedIn) {
            console.log("loggedIn: ", loggedIn)
            logIn();
        } else {
            console.log("already logged in");
        }

    }

    async function logIn() {
        try {
            const token = await createSession(email, password, props);
            localStorage.setItem("user", JSON.stringify({email: email, token: token}));
            props.setLoggedIn(true);
            props.setEmail(email);

            navigate("/");

        } catch (e) {
            console.log(e);
        }

    }

    return <div className={"mainContainer"}>

        <div className={"titleContainer"}>

            <div>Login</div>

        </div>

        <br />

        <div className={"inputContainer"}>

            <input

                value={email}

                placeholder="Enter your email here"

                onChange={ev => setEmail(ev.target.value)}

                className={"inputBox"} />

            <label className="errorLabel">{emailError}</label>

        </div>

        <br />

        <div className={"inputContainer"}>

            <input

                value={password}

                placeholder="Enter your password here"

                onChange={ev => setPassword(ev.target.value)}

                className={"inputBox"} />

            <label className="errorLabel">{passwordError}</label>

        </div>

        <br />

        <div className={"inputContainer"}>

            <input

                className={"inputButton"}

                type="button"

                onClick={onButtonClick}

                value={"Log in"} />

        </div>

    </div>

}


export default Login
