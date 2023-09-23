import axios from "axios";
import config from "tailwindcss/defaultConfig";

const URL_API_FILE = "http://localhost:8082/convert/xmlToJson";
const URL_API_TESTE = "http://localhost:8082/convert/xmlToJson";
const URL_API_CLIENT = "http://localhost:8082/notafiscal";


const URL_API_FILE_NGROK = "https://e7f4-2804-1b3-9402-40e8-a8d7-47e6-38c0-95f7.ngrok-free.app/convert/xmlToJson"
const URL_API_FILE_CLIENT = "https://e7f4-2804-1b3-9402-40e8-a8d7-47e6-38c0-95f7.ngrok-free.app/notafiscal"


export async function sendFileXML(file)
{
    const config = { headers: { 'Content-Type': 'multipart/form-data', "ngrok-skip-browser-warning": "69420" } };
    return axios.post(URL_API_FILE, file, config)
}

export async function searchClient(value)
{
    const config = { headers: { "ngrok-skip-browser-warning": "69420" } };
    return axios.get(URL_API_CLIENT + "/" + value, config)
}

export async function teste()
{
    const config = { headers: { 'Content-Type': 'multipart/form-data' } };
    return axios.post(URL_API_TESTE)
}


