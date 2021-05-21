<template>
  <div>
    <!-- サイドバー・検索 -->
    <div class="row">
      <div id="sidebar" class="col-3 col-xl-3 col-xxl-2">
        <h2>RAMNOTE</h2>

        <input class="form-control" type="text" />
        <button class="form-control">Search</button>

        <label class="form-label">Tags</label>
        <input
          id="formTags"
          class="form-control"
          type="text"
          :value="query_tags_str()"
        />

        <label class="form-label">From</label>
        <input class="form-control" type="date" />

        <label class="form-label">To</label>
        <input class="form-control" type="date" />

        <button
          class="form-control"
          data-bs-toggle="modal"
          data-bs-target="#editorCreate .modal"
        >
          Add
        </button>
      </div>

      <!-- ノート一覧 -->
      <div id="contents" class="col-9 col-xl-9 col-xxl-10 ms-auto">
        <div class="row justify-content-center">
          <NoteCard
            v-for="note in notes"
            :key="note.id"
            :note="note"
            class="col-5 col-xl-4 col-xxl-2 m-2"
          ></NoteCard>
        </div>
      </div>
    </div>

    <!-- タグ選択画面 -->
    <div id="tagPickerQuery">
      <TagPicker v-model="query_tags"></TagPicker>
    </div>

    <!-- エディタ -->
    <div id="editorCreate">
      <Editor :note="newNote"></Editor>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import bootstrap from "bootstrap"

import NoteCard from "./components/NoteCard.vue"
import TagPicker from "./components/TagPicker.vue"
import Editor from "./components/NoteEditor.vue"
import { Note, Tag } from "./model"
import { dao } from "./dao"

@Options({
  components: {
    NoteCard,
    TagPicker,
    Editor,
  },
})
export default class App extends Vue {
  notes: Note[] = []  // 表示するノート
  newNote = Note.empty()

  query_tags: Tag[] = []
  query_tags_str = () => this.query_tags.map(tag => tag.name).join(' ')

  mounted(): void {
    // タグ入力フォームをクリックすると、タグ選択画面を開く
    const formTags = document.getElementById('formTags')
    if (formTags) {
      formTags.addEventListener('click', (e) => {
        e.preventDefault()
        formTags.blur()

        // ダイアログを開く
        const tagPicker = document.querySelector('#tagPickerQuery .modal')
        if (tagPicker) {
          console.log(tagPicker)
          let modal = new bootstrap.Modal(tagPicker)
          modal.show()
        }
      })
    }

    // サンプルデータを設定
    // this.notes = []
    // samplenotes.forEach((note) => {
    //   this.notes.push(note)
    // })

    dao.getNotes()
      .then(notes => {
        notes.forEach(note => {
          this.notes.push(note)
        })
      })

  }
}

let samplenotes: Note[] = [
  {
    id: '0',
    title: 'asdf',
    body: 'fwfgxfgvf',
    date: new Date(124),
    tags_str: ['67375', '34653',]
  },
  {
    id: '1',
    title: 'kiuitglor',
    body: 'wery45ujrf',
    date: new Date(3245),
    tags_str: ['735', '6704',]
  },
  {
    id: '2',
    title: 'dsgwet45j',
    body: 'syrtqt43w',
    date: new Date(876),
    tags_str: ['53546', '4376',]
  },
  {
    id: '3',
    title: 'sbdfhjdt',
    body: 'ear54hss',
    date: new Date(5638),
    tags_str: ['3764', '556798',]
  },
]

</script>

<style>
#sidebar {
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;

  background-color: #ff9999;
}
#contents {
  background-color: #9999ff;
}
</style>
