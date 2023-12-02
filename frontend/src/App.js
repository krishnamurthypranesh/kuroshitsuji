import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import Home from './home';

import Login from './login';

import Navbar from './navigation/Navigation';

import PrivateRoute from './PrivateRoute';

import CreateCollection from './CreateCollection';

import './App.css';

import { useEffect, useState, useLayoutEffect } from 'react';

function App() {
  const checkSession = () => {
    const user = JSON.parse(localStorage.getItem("user"))

    if (!user || !user.token) {
      // make a call to check the validity of the session here
      return false
    }

    return true
  }

  const [loggedIn, setLoggedIn] = useState(checkSession());
  const [email, setEmail] = useState("");

  useLayoutEffect(() => {
    const _loggedIn = checkSession();
    setLoggedIn(_loggedIn);
  }, [])


  console.log("1. before running checkSession: ", loggedIn);
  checkSession();
  console.log("2. after running checkSession: ", loggedIn);

  return (
      <div className="App">

      {loggedIn && <Navbar />}

      <BrowserRouter>

        <Routes>

          <Route
            exact
            path="/login"
            element={
              !loggedIn ? (
                <Login loggedIn={loggedIn} setLoggedIn={setLoggedIn} setEmail={setEmail} />
              ) : (
                <Navigate replace to={"/"} />
              )}
            />

          <Route exact path='/' element={<PrivateRoute component={Home} loggedIn={loggedIn} />}>
            <Route exact path='/' element={<Home loggedIn={loggedIn} setLoggedIn={setLoggedIn} />}/>
          </Route>

          <Route exact path='/collections/new' element={<PrivateRoute component={CreateCollection} loggedIn={loggedIn} />}>
            <Route path="/collections/new" element={<CreateCollection />} />
          </Route>

        </Routes>

      </BrowserRouter>

    </div>
  )
}

export default App;
