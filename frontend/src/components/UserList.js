export const UserItem = ({ item }) => {
    return (
        <tr>
            <td>{ item.username }</td>
            <td>{ item.first_name }</td>
            <td>{ item.last_name }</td>
            <td>{ item.email }</td>
        </tr>
    )
}


const UserList = ({ users }) => {
    return (
        <table>
            <thead>
                <tr>
                    <th>Username</th>
                    <th>First name</th>
                    <th>Last name</th>
                    <th>E-mail</th>
                </tr>
            </thead>
            <tbody>
                { users.map( user => <UserItem key={ user.username } item={ user }/> ) }
            </tbody>
        </table>
    )
}

export default UserList;
