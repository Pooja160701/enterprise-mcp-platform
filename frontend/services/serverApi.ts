import { api } from "./api";

export async function getServers() {

    const response = await api.get("/servers");

    return response.data;

}