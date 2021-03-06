import { consts } from "./consts";

export class config {
    static get apiRoot() {
        if (process.env.IS_ELECTRON) {
            return `http://127.0.0.1:${consts.serverPort}/api/`
        }
        return '/api/'
    }

    private constructor() { return false }
}
