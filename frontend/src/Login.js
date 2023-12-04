import React, { useState } from "react";

import { useNavigate } from "react-router-dom";


export async function createSession(email, password, props) {
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

    const response = await fetch(
        "http://localhost:8000/v1/authn/user-sessions/",
        {
            method: "DELETE",
            headers: {
                "Authorization": "Bearer " + userToken,
                "Content-Type": "application/json",
            },
        }
    );

    if (!response.ok) {
        console.log(response);
        throw new Error("failed to login");
    }

    return true
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

        logIn();

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

    if (loggedIn) {
        console.log("already logged in");
        navigate("/");
    }

    return <div className={"mainContainer"}>

        <div className={"titleContainer"}>

            <div>Login</div>

        </div>

        <br />

        <div className={"inputContainer"}>
            <form>
                <div className="form-group">
                    <input type="email" className="form-control" id="login-email" placeholder="jhon@doe.com" onChange={ev => setEmail(ev.target.value)} />
                    <label className="errorLabel">{emailError}</label>
                </div>

                <div className="form-group">
                    <input type="password" className="form-control" id="login-password" placeholder="password" onChange={pv => setPassword(pv.target.value)} />
                    <label className="errorLabel">{passwordError}</label>
                </div>

                <button type="button" className="btn btn-primary" onClick={onButtonClick}>Log In</button>
            </form>

        </div>

    </div>

}


export default Login
