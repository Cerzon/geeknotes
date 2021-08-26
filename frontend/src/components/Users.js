const UserItem = ({ user }) => {
    return (
        <tr>
            <td>{ user.username }</td>
            <td>{ user.first_name }</td>
            <td>{ user.last_name }</td>
            <td>{ user.email }</td>
        </tr>
    )
}


const UserList = ({ users }) => {
    const usersElements = users.map( (user) => <UserItem user={ user }/> );
    return (
        <table>
            <tr>
                <th>Username</th>
                <th>First name</th>
                <th>Last name</th>
                <th>E-mail</th>
            </tr>
            { usersElements }
        </table>
    )
}

export default UserList;