import React from "react"

import { useNavigate } from "react-router-dom";

import {deleteSession} from "./login";


const Home = (props) => {

    // this would be better if placed under the nav bar
    const { loggedIn, setLoggedIn } = props

    const navigate = useNavigate();

    const onCreateCollectionButtonClick = () => {
        navigate("/collections/new");
    }

    // the layout of this page is pretty simple
    // load the collections table
    // show a button above the collections table showing a place for adding new collections
    // show a table listing all collections for this user account

    return (
        <div>
            <button type="button" class="btn btn-outline-primary" onClick={onCreateCollectionButtonClick}>Create Collection</button>
            <table class="table">
                <thead>
                    <tr>
                    <th scope="col">#</th>
                    <th scope="col">First</th>
                    <th scope="col">Last</th>
                    <th scope="col">Handle</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                    <th scope="row">1</th>
                    <td>Mark</td>
                    <td>Otto</td>
                    <td>@mdo</td>
                    </tr>
                    <tr>
                    <th scope="row">2</th>
                    <td>Jacob</td>
                    <td>Thornton</td>
                    <td>@fat</td>
                    </tr>
                    <tr>
                    <th scope="row">3</th>
                    <td>Larry</td>
                    <td>the Bird</td>
                    <td>@twitter</td>
                    </tr>
                </tbody>
            </table>
        </div>
    )
}


export default Home
