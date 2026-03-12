module Jekyll
  class TagFeedPage < Page
    def initialize(site, base, dir, name, tag, title)
      @site = site
      @base = base
      @dir = dir
      @name = name

      self.process(@name)
      self.data = {
        "layout" => "feed",
        "feed_tag" => tag,
        "feed_title" => title,
      }
    end
  end

  class TagFeedGenerator < Generator
    safe true

    def generate(site)
      title = site.config["title"]
      tags = site.collections["notes"].docs
        .flat_map { |doc| doc.data["tags"] || [] }
        .uniq

      tags.each do |tag|
        site.pages << TagFeedPage.new(
          site, site.source,
          "feed", "#{tag}.xml",
          tag, "#{title} - #{tag}"
        )
      end

      # feed/everything.xml — all posts, no tag filter
      site.pages << TagFeedPage.new(
        site, site.source,
        "feed", "everything.xml",
        nil, title
      )

      # feed.xml — alias for feed/recommended.xml
      site.pages << TagFeedPage.new(
        site, site.source,
        "", "feed.xml",
        "recommended", "#{title} - recommended"
      )
    end
  end
end
