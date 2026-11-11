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
