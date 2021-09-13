import { Redirect } from "react-router-dom";


const Logout = ({ removeToken, is_authenticated }) => {
    return (
        is_authenticated
        ? <div>
            <h2>Are you sure you want to logout?</h2>
            <button onClick={ removeToken }>Confirm</button>
        </div>
        : <Redirect push to='/' />
    )
}


export default Logout;
