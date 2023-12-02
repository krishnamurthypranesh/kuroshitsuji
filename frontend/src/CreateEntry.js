import { React, useEffect, useState } from "react";

import { useNavigate, useParams } from "react-router-dom";

const CreateEntry = (props) => {
    const urlParams = useParams();

    const [collection, setCollection] = useState({});
    const [entryContent, setEntryContent] = useState("");

    useEffect(() => { getCollectionById() }, [])

    const navigate = useNavigate();

    const onSaveButtonClick = () => {
        // navigate to the concerned url
        navigate("/collections/" + urlParams.collectionId + "/new-entry/")
    }

    const onPublishButtonClick = () => {}

    async function getCollectionById() {
        // const userToken = JSON.parse(localStorage.getItem("user")).token;

        // const response = await fetch(
        //     "http://localhost:8000/v1/journal/collections/" + urlParams.collectionId,
        //     {
        //         method: "GET",
        //         headers: {
        //             Authorization: "Bearer " + userToken,
        //             "Content-Type": "application/json",
        //         },
        //     }
        // )
        // if (!response.ok) {
        //     console.log("error fetching data from server");
        //     throw new Error("error fetching data from server");
        // }

        // const data = await response.json();

        const data = {
            collection_id: urlParams.collectionId,
            name: "test_e59m",
            template: {
                fields: [
                    {
                        key: "title",
                        display_name: "Title",
                    },
                    {
                        key: "content",
                        display_name: "Content",
                    },
                ]
            },
            active: true,
            created_at: "2023-12-02T18:10:33Z",
        }

        setCollection(data)
    }

    const renderForm = () => {
        return (
        <form>
            <div className="form-group">
                <label for="collectionEntry">Title</label>
                <input type="email" className="form-control" id="collectionEntry" aria-describedby="emailHelp" placeholder="Enter title"></input>
                <small id="emailHelp" className="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div className="form-group">
                <label for="CollectionEntry">Password</label>
                <input type="password" className="form-control" id="CollectionEntry" placeholder="Password"></input>
                <textarea id="entry-content" name="textarea" value={entryContent} onChange={(e) => {setEntryContent(e.target.value)}} cols={100} rows={10} style={{width: "100%"}}/>
            </div>
            <div className="form-group form-check">
                <input type="checkbox" className="form-check-input" id="publish-entry-checkbox"></input>
                <label className="form-check-label" for="publish-entry-checkbox">Publish this</label>
            </div>
            <button type="submit" className="btn btn-primary">Save Entry</button>
        </form>
        )
    }

    return renderForm()
}

export default CreateEntry;
