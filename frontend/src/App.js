import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';

import Home from './Home';

import Login from './Login';

import Navbar from './navigation/Navigation';

import PrivateRoute from './PrivateRoute';

import CreateCollection from './CreateCollection';

import CollectionDetails from './CollectionDetails';

import CreateEntry from './CreateEntry';

import EntryDetails from './EntryDetails';

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


  checkSession();

  return (
      <div className="App container-fluid" id="main-container">

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

          {/* <Route exact path='/collections/new' element={<PrivateRoute component={CreateCollection} loggedIn={loggedIn} />}>
            <Route path="/collections/new" element={<CreateCollection />} />
          </Route> */}

          <Route exact path='/collections/:collectionId' element={<PrivateRoute component={CollectionDetails} loggedIn={loggedIn} />}>
            <Route path="/collections/:collectionId" element={<CollectionDetails />} />
          </Route>

          <Route exact path='/collections/:collectionId/new-entry' element={<PrivateRoute component={CreateEntry} loggedIn={loggedIn} />}>
            <Route path="/collections/:collectionId/new-entry" element={<CreateEntry />} />
          </Route>

          <Route exact path='/entries/:entryId' element={<PrivateRoute component={EntryDetails} loggedIn={loggedIn} />}>
            <Route path="/entries/:entryId" element={<EntryDetails />} />
          </Route>


        </Routes>

      </BrowserRouter>

    </div>
  )
}

export default App;
