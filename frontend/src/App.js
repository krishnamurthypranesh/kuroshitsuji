import { BrowserRouter, Route, Routes } from 'react-router-dom';

import Home from './home';

import Login from './login';

import Navbar from './navigation/Navigation';

import PrivateRoute from './PrivateRoute';

import CreateCollection from './CreateCollection';

import './App.css';

import { useEffect, useState, useLayoutEffect } from 'react';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [email, setEmail] = useState("");

  useEffect(() => {
    const user = JSON.parse(localStorage.getItem("user"))

    if (!user || !user.token) {
      setLoggedIn(false)
      return
    } else {
      setLoggedIn(true)
    }
  }, [])

  console.log("before returning app: ", loggedIn);

  return (
      <div className="App">

      {loggedIn && <Navbar />}

      <BrowserRouter>

        <Routes>

          <Route exact path='/' element={<PrivateRoute loggedIn={loggedIn} />}>
            <Route exact path='/' element={<Home loggedIn={loggedIn} setLoggedIn={setLoggedIn} />}/>
          </Route>

          <Route exact path='/collections/new' element={<PrivateRoute loggedIn={loggedIn} />}>
            <Route path="/collections/new" element={<CreateCollection />} />
          </Route>

          { !loggedIn && <Route path="/login" element={<Login setLoggedIn={setLoggedIn} setEmail={setEmail} />} /> }

        </Routes>

      </BrowserRouter>

    </div>
  )
}

export default App;
