const { VK } = require('vk-io');
const vk = new VK();
const users = require('./users.json')
const fs = require('fs');
vk.setOptions({
token:"308c84f2960c5f757b0bdd16e6e3200000000000000003d93677516c80ca323ac0edeaf570bc7b1f99664"
});

const works = [
  {
    name: 'Дворник',
    id: 1,
    money: 1000
  },
  {
    name: 'Кассир',
    id: 2,
    money: 2000
  },
  {
    name: 'Таксист',
    id: 3,
    money: 5000
  }
]

function timeLeft(stamp) {
  stamp -= Date.now()
  stamp = stamp / 1000;
  let s = stamp % 60;
  stamp = ( stamp - s ) / 60;
  let m = stamp % 60;
  stamp = ( stamp - m ) / 60;
  let h = ( stamp ) % 24;
  let d = ( stamp - h ) / 24;
  let text = ``;
  if(d > 0) text += Math.floor(d) + " д. ";
  if(h > 0) text += Math.floor(h) + " ч. ";
  if(m > 0) text += Math.floor(m) + " мин. ";
  if(s > 0) text += Math.floor(s) + " с.";
  return text;
}

setInterval(async () => {
    fs.writeFileSync("./users.json", JSON.stringify(users, null, "\t"))
}, 500);

vk.updates.on(['new_message'], (next, context) => {
  if(users.filter(x => x.id === next.senderId)[0]) return context()
  users.push({
    id: next.senderId,
    balance: 5000,
    work: {
      timer: 0,
      name: 'Нет',
      id: 0,
      day: 0
    },
    nick: 'Игрок'
  })
  return context()
})

vk.updates.hear(/^проф/i, msg => {
  user = users.filter(x => x.id === msg.senderId)[0]
  msg.send(`${user.nick}, вот твой профиль:\n  Баланс: ${user.balance}\n  Работа: ${user.work.name}`)
})

vk.updates.hear(/^работы$/i, msg => {
  user = users.filter(x => x.id === msg.senderId)[0]
  msg.send(`${user.nick}, вот все доступные работы:\n1. Дворник [1.000]\n2. Кассир [2.000]\n3. Таксист [5.000]\n\nЧтобы устроиться на работу, введи: "Работа [номер работы]"`)
})

vk.updates.hear(/^работа ([0-9]+)/i, msg => {
  user = users.filter(x => x.id === msg.senderId)[0]
  num = Number(msg.$match[1])
  if(num > 3 || num < 1) return msg.send(`Неверный номер работы!`)
  work = works.filter(x => x.id === num)[0]
  user.work.name = work.name
  user.work.id = work.id
  msg.send(`${user.nick}, вы устроились на работу "${work.name}"`)
})

vk.updates.hear(/^работать$/i, msg => {
  user = users.filter(x => x.id === msg.senderId)[0]
  if(user.work.timer > Date.now()) return msg.send(`${user.nick}, вы отработали неделю, осталось отдыхать: ${timeLeft(user.work.timer)}`)
  user.work.day++
  work = works.filter(x => x.id === user.work.id)[0]
  if(user.work.day == 5){
    user.work.day = 0
    user.work.timer = Date.now() + 60000
  }
  user.balance += work.money
  msg.send(`${user.nick}, рабочий день завершен, вы заработали: ${work.money}`)
})

vk.updates.hear(/^ник (.*)/i, msg => {
  user = users.filter(x => x.id === msg.senderId)[0]
  nick = msg.$match[1]
  if(nick.length > 15) return msg.send(`Ник не может быть длиннее 15 символов!`)
  user.nick = nick
  msg.send(`Вы сменили никнейм на "${nick}"`)
})

console.log("ok");
vk.updates.start().catch(console.error);