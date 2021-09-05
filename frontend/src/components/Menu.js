import { Link } from "react-router-dom";


const Menu = ({ links }) => {
    return (
        <nav className='top-menu'>
            { links.map( item => <Link
                                    to={ item.href }
                                    key={ item.href }
                                    className='menu-item-link'
                                >
                                    { item.name }
                                </Link> ) }
        </nav>
    )
}

export default Menu;
