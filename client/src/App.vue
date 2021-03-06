<template>
  <div>
    <!-- サイドバー・検索 -->
    <div class="sidebar">
      <div class="p-2">
        <!-- ロゴ RAMNOTE -->
        <img
          src="@/assets/ramnote.svg"
          class="img-fluid pointer-cursor"
          style="cursor: pointer"
          @click="showInitialPage"
        />
      </div>

      <div class="p-2">
        <div class="mb-3">
          <label class="form-label">キーワード</label>
          <input
            type="search"
            class="form-control"
            style="-webkit-appearance: searchfield-cancel-button"
            v-model="keyword"
            @keydown="keydownAtKeywordInput"
          />
        </div>

        <div class="mb-3">
          <label class="form-label">タグ</label>
          <input
            id="formTags"
            class="form-control"
            type="text"
            placeholder="クリックで追加"
            readonly
            :value="query_tags_str"
            @click="openTagPicker"
          />
        </div>

        <button class="mb-3 btn btn-light form-control" @click="fetchNotes">
          検索
        </button>

        <div class="mb-3 pt-3 border-top">
          <button class="btn btn-light form-control" @click="showEditorCreate">
            メモを追加
          </button>
        </div>
      </div>

      <div class="p-2" style="position: absolute; bottom: 0; width: 100%">
        <a :href="csvUrl" class="btn btn-light form-control">
          CSVエクスポート
        </a>
      </div>

      <!--
          実装予定の日時検索
        <label class="form-label">From</label>
        <input class="form-control" type="date" />

        <label class="form-label">To</label>
        <input class="form-control" type="date" />
        -->
    </div>

    <!-- メインカラム -->
    <div class="contents overflow-scroll">
      <!-- アラート -->
      <div class="alert alert-success" v-show="successMsg">
        {{ successMsg }}
      </div>
      <div class="alert alert-danger" v-show="errorMsg">
        {{ errorMsg }}
      </div>

      <!-- ノート一覧画面 -->
      <div
        class="d-flex flex-wrap notelist"
        v-if="currentTab == tabname.notelist"
      >
        <NoteCard
          class="m-1"
          v-for="note in notes"
          :key="note.id"
          :note="note"
          @edit="showEditPage"
          @delete="comfirmDeleteNote"
        ></NoteCard>
        <div class="note-empty m-1"></div>
        <div class="note-empty m-1"></div>
        <div class="note-empty m-1"></div>
        <div class="note-empty m-1"></div>
        <div class="note-empty m-1"></div>
      </div>

      <!-- ノート作成画面 -->
      <div class="editor" v-if="currentTab == tabname.editor">
        <NoteEditor
          :note="editNote"
          @cancel="currentTab = tabname.notelist"
          @create="commitCreate"
          @update="commitUpdate"
        ></NoteEditor>
      </div>
    </div>
  </div>

  <!-- 検索用タグ選択画面 -->
  <div id="tagPickerQuery">
    <TagPicker
      :tags="query_tags"
      :visible="isOpenTagPicker"
      @close="tagPickerClosed"
    ></TagPicker>
  </div>

  <!-- 削除確認ダイアログ -->
  <div id="deleteDialog" class="modal" tabindex="-1">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-body">
          <p>削除してもよろしいですか？</p>
        </div>
        <div class="modal-footer">
          <button data-bs-dismiss="modal" class="btn btn-primary">
            Cancel
          </button>
          <button
            data-bs-dismiss="modal"
            class="btn btn-danger"
            @click="commitDelete"
          >
            OK
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import bootstrap from "bootstrap";

import NoteCard from "./components/NoteCard.vue";
import TagPicker from "./components/TagPicker.vue";
import NoteEditor from "./components/NoteEditor.vue";
import { Note, Tag } from "./models";
import { dao } from "./dao";
import { config } from "./config";

@Options({
  components: {
    NoteCard,
    TagPicker,
    NoteEditor,
  },
})
export default class App extends Vue {
  readonly tabname = {
    notelist: "notelist",
    editor: "editor",
  };

  notes: Note[] = []; // 表示するノート
  editNote: Note = Note.empty();

  query_tags: Tag[] = [];
  currentQueryTags: Tag[] = [];
  keyword = "";
  currentKeyword = "";

  currentTab = this.tabname.notelist; // メインカラムに表示するもの
  successMsg = "";
  errorMsg = "";
  isOpenTagPicker = false;

  // タグをスペースで結合した形式に変換
  get query_tags_str(): string {
    return this.query_tags.map((tag) => tag.name).join(" ");
  }

  get csvUrl(): string {
    let tagIds = this.currentQueryTags.map((tag) => tag.id).join(",");
    let params = "";
    params += "keyword=" + encodeURIComponent(this.currentKeyword);
    params += "&tag-ids=" + encodeURIComponent(tagIds);
    return config.apiRoot + "export/csv?" + params;
  }

  flashError(msg: string, time = 3): void {
    this.errorMsg = msg;
    setTimeout(() => (this.errorMsg = ""), time * 1000);
  }
  flashSuccess(msg: string, time = 3): void {
    this.successMsg = msg;
    setTimeout(() => (this.successMsg = ""), time * 1000);
  }

  keydownAtKeywordInput(e: KeyboardEvent): void {
    if (e.key == "Enter") {
      this.fetchNotes();
    }
  }

  tagPickerClosed(): void {
    this.isOpenTagPicker = false;
    this.fetchNotes();
  }

  showInitialPage(): void {
    this.keyword = "";
    this.query_tags = [];
    this.fetchNotes();
    this.currentTab = this.tabname.notelist;
  }

  // タグ選択フォームがクリックされた時
  openTagPicker(e: MouseEvent): void {
    e.preventDefault();
    (e.target as HTMLElement).blur();
    this.isOpenTagPicker = true;
  }

  showEditorCreate(e: MouseEvent): void {
    this.editNote = Note.empty();
    this.currentTab = this.tabname.editor;
  }

  showEditPage(note: Note): void {
    this.editNote = note.clone();
    this.currentTab = this.tabname.editor;
  }

  comfirmDeleteNote(note: Note): void {
    // 削除確認ダイアログを開く
    const dialog = document.querySelector("#deleteDialog");
    if (dialog) {
      this.editNote = note.clone();
      let modal = new bootstrap.Modal(dialog);
      modal.show();
    }
  }

  fetchNotes(retry = 0): void {
    dao
      .getNotes(this.keyword, this.query_tags)
      .then((notes) => {
        this.notes = notes;
        this.currentKeyword = this.keyword;
        this.currentQueryTags = this.query_tags;
      })
      .catch((err) => {
        this.flashError(err.result);

        // リトライ処理
        // Electronの初期読み込みに、Serverの初期化が間に合ってないとき
        // エラーが帰ってくる
        if (retry > 0) {
          new Promise((r) => setTimeout(r, 1000)).then(() =>
            this.fetchNotes(retry - 1)
          );
        }
        if (retry == 0) {
          console.log(err);
        }
        // 開発環境の場合は、ダミーデータを表示
        // if (process.env.NODE_ENV == 'development') {
        //   this.notes = consts.dummyNotes.slice()
        // }
      });
  }

  commitDelete(): void {
    if (this.editNote.id) {
      dao
        .deleteNote(this.editNote)
        .then((res) => {
          this.fetchNotes();
          this.flashSuccess("削除しました");
        })
        .catch((err) => {
          this.flashSuccess("失敗しました\n" + err.result);
        });
    }
  }

  commitCreate(): void {
    if (this.editNote.id == null) {
      // id が null の時は新規作成
      this.editNote.date = new Date(); // 改めて現在日時を格納
      dao
        .createNote(this.editNote)
        .then((res) => {
          this.fetchNotes();
          this.flashSuccess("追加しました");
          this.editNote = Note.empty();
        })
        .catch((err) => {
          this.flashSuccess("失敗しました\n" + err.result);
        });
    }
  }

  commitUpdate(): void {
    if (this.editNote.id != null) {
      dao
        .updateNote(this.editNote)
        .then((res) => {
          this.fetchNotes();
          this.flashSuccess("更新しました");
          this.currentTab = this.tabname.notelist;
        })
        .catch((err) => {
          this.flashSuccess("失敗しました\n" + err.result);
        });
    }
  }

  mounted(): void {
    this.fetchNotes(50);
  }
}
</script>

<style scoped>
button:focus,
.btn:focus {
  outline: none !important;
  box-shadow: none !important;
}
.sidebar {
  z-index: 100;
  position: fixed;
  top: 0;
  left: 0;
  bottom: 0;
  width: 200px;

  color: #ffffff;
  background-color: #313131;
}
.contents {
  z-index: 100;
  position: fixed;
  top: 0;
  bottom: 0;
  left: 200px;
  right: 0;
  padding: 10px;
  background-color: #fafafa;
}
.contents[display="none"] {
  display: none;
}
.notelist {
  display: grid;
  gap: 10px;
  justify-content: center;
  grid-template-columns: repeat(auto-fit, 1fr);
}
.note-empty {
  display: block;
  width: 320px;
  content: "";
}
.alert {
  z-index: 10000;
  position: fixed;
  bottom: 0;
  left: 200px;
  right: 0;
  margin: 10px;
}
</style>
