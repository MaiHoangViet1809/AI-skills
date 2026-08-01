(() => {
  const MAX_ELEMENTS = 300;
  const MAX_TEXT = 80;
  const IMPORTANT_TAGS = new Set([
    "a",
    "button",
    "input",
    "select",
    "textarea",
    "header",
    "nav",
    "main",
    "section",
    "article",
    "footer",
    "h1",
    "h2",
    "h3",
    "p",
    "li"
  ]);

  const clip = (value, limit = MAX_TEXT) => {
    const text = String(value || "").replace(/\s+/g, " ").trim();
    return text.length > limit ? `${text.slice(0, limit)}...` : text;
  };

  const selectorFor = (element) => {
    if (!(element instanceof Element)) return "";
    const parts = [];
    let current = element;
    while (current && current.nodeType === Node.ELEMENT_NODE && parts.length < 4) {
      let part = current.tagName.toLowerCase();
      if (current.id) {
        part += `#${CSS.escape(current.id)}`;
        parts.unshift(part);
        break;
      }
      const classes = Array.from(current.classList || []).slice(0, 3);
      if (classes.length) part += `.${classes.map((name) => CSS.escape(name)).join(".")}`;
      parts.unshift(part);
      current = current.parentElement;
    }
    return parts.join(" > ");
  };

  const isVisible = (element) => {
    const rect = element.getBoundingClientRect();
    const style = getComputedStyle(element);
    return (
      rect.width > 0 &&
      rect.height > 0 &&
      style.visibility !== "hidden" &&
      style.display !== "none" &&
      Number(style.opacity) !== 0
    );
  };

  const styleFor = (element) => {
    const style = getComputedStyle(element);
    const rect = element.getBoundingClientRect();
    return {
      color: style.color,
      backgroundColor: style.backgroundColor,
      borderColor: style.borderColor,
      borderWidth: style.borderWidth,
      borderRadius: style.borderRadius,
      boxShadow: style.boxShadow,
      fontFamily: style.fontFamily,
      fontSize: style.fontSize,
      fontWeight: style.fontWeight,
      lineHeight: style.lineHeight,
      letterSpacing: style.letterSpacing,
      margin: style.margin,
      padding: style.padding,
      display: style.display,
      gap: style.gap,
      width: `${Math.round(rect.width)}px`,
      height: `${Math.round(rect.height)}px`
    };
  };

  const tokenVariables = Array.from(document.styleSheets)
    .flatMap((sheet) => {
      try {
        return Array.from(sheet.cssRules || []);
      } catch {
        return [];
      }
    })
    .flatMap((rule) => {
      const style = rule.style;
      if (!style) return [];
      return Array.from(style)
        .filter((name) => name.startsWith("--"))
        .map((name) => ({
          name,
          value: style.getPropertyValue(name).trim(),
          selector: rule.selectorText || ""
        }));
    });

  const elements = Array.from(document.querySelectorAll("body *"))
    .filter((element) => {
      if (!isVisible(element)) return false;
      if (IMPORTANT_TAGS.has(element.tagName.toLowerCase())) return true;
      const role = element.getAttribute("role");
      return Boolean(role || element.className);
    })
    .slice(0, MAX_ELEMENTS)
    .map((element, index) => ({
      id: `element-${index + 1}`,
      tag: element.tagName.toLowerCase(),
      role: element.getAttribute("role") || "",
      selector: selectorFor(element),
      text_sample: clip(element.textContent),
      styles: styleFor(element)
    }));

  return {
    schema_version: "design-mirror-web-collector/v1",
    url: location.href,
    title: document.title,
    viewport: {
      width: innerWidth,
      height: innerHeight,
      device_pixel_ratio: devicePixelRatio
    },
    color_scheme: matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light",
    token_variables: tokenVariables,
    elements,
    limitations: [
      "Does not inspect cross-origin frames.",
      "Does not force pseudo-states.",
      "Does not extract canvas, WebGL, or closed shadow-root internals."
    ]
  };
})();
