// This is used to determine if a user is authenticated and
// if they are allowed to visit the page they navigated to.

// If they are: they proceed to the page
// If not: they are redirected to the login page.
import React from 'react'
// import AuthService from './Services/AuthService'
import { Navigate, Outlet } from 'react-router-dom'

const PrivateRoute = ({ component: Component, loggedIn, ...rest }) => {

  // Add your own authentication on the below line.
//   const isLoggedIn = AuthService.isLoggedIn()
    console.log("private_route: loggedIn", loggedIn);
    return loggedIn ? <Outlet /> : <Navigate to="/login" />;
}

export default PrivateRoute
