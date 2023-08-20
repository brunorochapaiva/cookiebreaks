import axios from "axios"
import { Dispatch, SetStateAction } from "react"
import { CookieBreak, User } from "./structs"

const dateOrUndefined = (datetime: string | undefined) =>
    datetime ? new Date(datetime) : undefined

export const getToken = async (
    username: string,
    password: string,
    setToken: Dispatch<SetStateAction<string>>,
    setUser: Dispatch<SetStateAction<User | undefined>>,
    setStatus: Dispatch<SetStateAction<string>>
) => {
    let endpoint = `/api/token`
    let data = new FormData()
    data.append("username", username)
    data.append("password", password)
    data.append("grant_type", "")
    data.append("client_id", "")
    data.append("client_secret", "")
    try {
        let response = await axios.post(endpoint, data)
        let responseData = response.data
        setToken(responseData.access_token)
        setUser({ user: username, admin: responseData.admin })
    } catch (err) {
        setStatus("Could not log in...")
    }
}

export const getBreaks = async (
    setBreaks: Dispatch<SetStateAction<CookieBreak[]>>
) => {
    let endpoint = `/api/breaks`
    let response = await axios.get(endpoint)
    let data = response.data
    let breaks = data.map((b: any) => ({
        id: b.id,
        host: b.host,
        datetime: new Date(b.break_time),
        location: b.location,
        cost: b.cost,
        announced: dateOrUndefined(b.break_announced),
        reimbursed: dateOrUndefined(b.host_reimbursed),
        claimed: dateOrUndefined(b.admin_claimed),
        success: dateOrUndefined(b.admin_reimbursed),
    }))
    setBreaks(breaks)
}
