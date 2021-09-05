export const Active = () => {
    return (
        <svg 
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 26 26"
        >
            <g strokeWidth="3" stroke="green" fill="none">
                <circle cx="13" cy="13" r="10" />
                <path d="M8 13l5 5l5-10" />
            </g>
        </svg>
    )
}


export const Closed = () => {
    return (
        <svg 
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 26 26"
        >
            <g strokeWidth="3" stroke="red" fill="none">
                <circle cx="13" cy="13" r="10" />
                <path d="M8 8l10 10m0-10l-10 10" />
            </g>
        </svg>
    )
}
