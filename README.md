# Blog
My assorted ramblings, concepts that I am trying to improve my understanding of,
and stuff that I made.

Take a look at the blog over at <https://unformeddelta.wiki>

## Image captions and alt text

`bin/publish-note` and `bin/sync-notes` use an image's caption as its default alt text when adding a new image without alt text. Exported images are associated with Photos only when the original filename (ignoring the extension) and capture time identify exactly one visible photo. If no unique match exists, embedded image metadata can supply a one-time default; the script reports that future Photos edits will not synchronize.

When an image already has different alt text, the prompt lets you use the Photos caption for both, save the alt text as the Photos caption, keep independent manual alt text, or write new manual alt text. A conflict without interactive input stops the command instead of silently choosing. Once unified, Photos is canonical: subsequent syncs overwrite the shared alt text from Photos, including when its caption is cleared.

The choice lives beside the image in the wiki note and is copied into the blog. A shared image looks like this:

```markdown
![Caption from Photos](images/IMG_6908.jpeg) <!-- photo-alt: 06E7091B-FEAF-42FF-8A34-5EEE0BD0522A -->
```

Add `manual` to preserve independent alt text, including deliberately empty alt text:

```markdown
![A tiny bit of the original airport brownie.](images/IMG_6908.jpeg) <!-- photo-alt: 06E7091B-FEAF-42FF-8A34-5EEE0BD0522A manual -->
```

Ordinary syncs leave existing unmarked images alone. To link an existing image or reconsider a manual/shared choice, run `bin/sync-notes --review-images <note-id>`. You can also edit the marker directly; removing `manual` makes Photos canonical again.

`bin/sync-photos` refreshes linked alt text in both the wiki and published blog without publishing unrelated wiki prose changes. Linked photos are excluded from its untriaged list. Standalone photo posts also use caption alt text by default; triage offers a manual alternative, and `bin/sync-photos publish <uuid> --alt "Description"` supplies one directly. Their markers live in the blog note because standalone photo posts have no wiki source.

All blog image exports have a maximum dimension of 2048 pixels, without upscaling smaller images. Photos-linked exports use `images/<UUID>-<fingerprint>.<extension>`, where the fingerprint is derived from the exported file. Identical exports share storage across notes and standalone photo posts; different crops, edits, or encodings stay separate. The UUID identifies the source photo, not its crop. Unmatched images retain their note-based names. HEIC is exported as JPEG and WebP as PNG.

Image export uses the wiki image or the standalone post's Photos source without substituting another rendition. A known UUID is enough to name the asset; export does not read SQLite. Photos lookup is used to discover missing UUIDs and refresh shared captions. A cover image's UUID is recorded as `image_photo:` in the wiki frontmatter, so it also works when there is no inline image marker.

`bin/migrate-images` prepares and checks a migration of existing exports; `--apply` writes the results, updates references, and removes replaced files. It preserves existing blog crops and alt text, adding manual source markers for matched wiki images. It does not push or commit changes. Existing captions can still be unified explicitly with `sync-notes --review-images`.
