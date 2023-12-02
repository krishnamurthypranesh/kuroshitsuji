import { React, useEffect, useState } from "react"

import { useNavigate } from "react-router-dom";


const Home = (props) => {
    const [collectionsList, setCollectionsList] = useState({ records: [] });

    useEffect(() => { listCollections() }, [])

    const navigate = useNavigate();

    const onCreateCollectionButtonClick = () => {
        navigate("/collections/new");
    }

    async function listCollections() {
        const userToken = JSON.parse(localStorage.getItem("user")).token;

        const response = await fetch(
            "http://localhost:8000/v1/journal/collections/?limit=10",
            {
                method: "GET",
                headers: {
                    "Authorization": "Bearer " + userToken,
                    "Content-Type": "application/json",
                }
            }
        );

        if (!response.ok) {
            console.log("error fetching data from server");
            throw new Error("error fetching data from server");
        }

        const data = await response.json();

        setCollectionsList(data)
    }

    const renderTable = () => {
        const data = collectionsList;

        const generateRow = (record, index) => {
            return (
                <tr>
                    <td>{index + 1}</td>
                    <td>{record.collection_id}</td>
                    <td>{record.name}</td>
                    <td>{record.created_at}</td>
                </tr>
            )
        }

        return (
            <div>
                <button type="button" className="btn btn-outline-primary" onClick={onCreateCollectionButtonClick}>Create Collection</button>

                <div className="row justify-content-center">
                    <table className="table table-responsive">
                        <thead>
                            <tr>
                            <th scope="col">Sl No</th>
                            <th scope="col">Collection ID</th>
                            <th scope="col">Name</th>
                            <th scope="col">Created At</th>
                            </tr>
                        </thead>
                        <tbody>
                            {
                                data.records.map((listValue, index) => {
                                    return generateRow(listValue, index)
                                })
                            }
                        </tbody>
                    </table>
                </div>
            </div>
        )
    }

    return renderTable()
}


export default Home
