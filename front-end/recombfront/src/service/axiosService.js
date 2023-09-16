import axios from "axios";

const URL_API_FILE = "http://localhost:8082/convert/xmlToJson";
const URL_API_TESTE = "http://localhost:8082/convert/xmlToJson";

export async function sendFileXML(file)
{
    const config = { headers: { 'Content-Type': 'multipart/form-data' } };
    return axios.post(URL_API_FILE, file, config)
}

export async function teste()
{
    const config = { headers: { 'Content-Type': 'multipart/form-data' } };
    return axios.post(URL_API_TESTE)
}


