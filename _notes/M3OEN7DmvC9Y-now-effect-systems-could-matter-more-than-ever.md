---
layout: post
title: "Now, effect systems could matter more than ever"
date: 2026-04-20 22:40 -0700
permalink: /M3OEN7DmvC9Y/now-effect-systems-could-matter-more-than-ever
redirect_from:
  - /M3OEN7DmvC9Y
tags: [effects, swift, agentic-programming, inkhaven]
---

Side-effects are where software gets risky. Most programming languages don't include effects in their type signatures.
```swift
func add(_ a: Int, _ b: Int) -> Int {
  launchTheMissiles()
  return a + b
}
```

Based just on the type signature `func add(_ a: Int, _ b: Int) -> Int` of this Swift function, it's impossible to know what happens inside of the function add.

As AI agents write a larger proportion of our software, the volume of code reviewed is getting larger and larger. Skimming type signatures is useful for getting a high level sense of whether the architecture is sensible. But without effects represented in the type system, it's hard to be confident that the type provides an accurate summary of the functions behavior.

Effect systems allow expressing side-effects a function's type signature. In Swift this might look something like this[^syntax-details]:
```swift
func add(_ a: Int, _ b: Int) {IO} -> Int {
  launchTheMissiles()
  return a + b
}

func launchTheMissiles() {IO} -> Void {
  // ... send a network request that launches a missile
}
```

[^syntax-details]: I represent effects as a set of capabilities just before the function arrow. This matches Swift's existing `async`/`throws` syntax for the effects it already represents in the type system, e.g. `func f() async throws -> Int`.

Just looking at just the type signature `func add(_ a: Int, _ b: Int) {IO} -> Int {` immediately signals that something suspicious is going on. A function that adds two numbers shouldn't need to perform any IO.

And with compiler support for effects, seeing the signature `func add(_ a: Int, _ b: Int) {} -> Int` (i.e. no effects) can guarantee that that the function doesn't perform any side effects. Haskell and some other functional programming languages are able to guarantee[^fine-print] pure functions are side-effect free.

[^fine-print]: There's a little bit of fine print. This requires [Safe Haskell](https://ghc.gitlab.haskell.org/ghc/doc/users_guide/exts/safe_haskell.html#safe-language) forbidding the use of `unsafePerformIO`, etc. which other breaks type safety. This is strong enough to implement [sandboxing](https://github.com/wooyakob/try-haskell) for haskell.org's "Try Haskell" widget.

More granular effects make it possible to capture more aspects of architecture at the effect level. Fairly detailed effect tracking through dependency injection is already fairly commonplace in OOP. The `@Dependency` injected `userService` and `analytics` here mark the "effects" that are available to the view model.
```swift
final class ProfileViewModel: ObservableObject {
    @Published private(set) var user: User?
    @Published private(set) var isLoading = false
    @Published private(set) var errorMessage: String?

    @Dependency(\.userService) private var userService
    @Dependency(\.analytics)   private var analytics

    private let userID: String
    init(userID: String) { self.userID = userID }

    @MainActor
    func load() async {
        isLoading = true
        defer { isLoading = false }
        analytics.track("profile_viewed", properties: ["user_id": userID])
        do {
            user = try await userService.loadProfile(userID)
        } catch {
            errorMessage = error.localizedDescription
            analytics.track("profile_load_failed", properties: ["user_id": userID])
        }
    }
}
```

In addition to making the `ProfileViewModel` more testable, injecting effects makes it possible to see what the `ProfileViewModel`'s dependencies are. And though compiler wouldn't prevent using `NSURLSession` directly from the `ProfileViewModel`, a code reviewer would likely notice and comment on such a change.

The need to review more code isn't the only way AI agents shift in favor of stronger effect tracking. The largest burden of using effect systems in practice is that they invite a lot of boilerplate. The `ProfileViewModel` example only requires a little more boilerplate than calling a global function, but compiler enforced effect annotations can require extra bookkeeping on every function declaration.

When updating a function to use a new effect, it's necessary to propagate that new effect annotation to all callers. AI agents are fairly good at automating a lot of this tedious work.

The shift to agentic programming makes reading code more important than ever. Representing which side-effects may be executed used to be fairly expensive, but is getting cheaper through the use of agents. Perhaps it is time to bring compiler enforced effect systems to main-stream programming languages.
