const uidLen = 32

export const util = Object.freeze({
    uid(): string {
        const nums = [...Array(uidLen).keys()].map(value => (Math.floor(Math.random() * 16)))
        const hex = nums.reduce(((s, num) => s + num.toString(16)), '')
        console.log(hex)
        return hex
    }
})