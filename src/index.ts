// mctop.org worker: canonicalise www -> apex, then serve static assets.
// The install script ships as a static asset (public/install) with a text/plain
// content-type via public/_headers, so the worker module carries no shell
// content (which the upload API's WAF rejects) and stays trivial.
interface Env {
  ASSETS: { fetch: (req: Request) => Promise<Response> };
}

export default {
  async fetch(req: Request, env: Env): Promise<Response> {
    const url = new URL(req.url);
    if (url.hostname.startsWith("www.")) {
      url.hostname = url.hostname.slice(4);
      return Response.redirect(url.toString(), 308);
    }
    return env.ASSETS.fetch(req);
  },
};
