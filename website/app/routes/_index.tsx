import landing from "~/images/landing.png"

export default function Index() {
  return (
    <div className="bg-gray-50">
      <div className="relative overflow-hidden">
        <main>
          <div className="bg-gray-900 pt-10 sm:pt-16 lg:overflow-hidden lg:pt-8 lg:pb-14">
            <div className="mx-auto max-w-7xl lg:px-8">
              <div className="lg:grid lg:grid-cols-2 lg:gap-8">
                <div className="mx-auto max-w-md px-6 sm:max-w-2xl sm:text-center lg:flex lg:items-center lg:px-0 lg:text-left">
                  <div className="lg:py-24">
                    <h1 className="mt-4 text-4xl font-bold tracking-tight text-white sm:mt-5 sm:text-6xl lg:mt-6 xl:text-6xl">
                      <span className="block">Sopic</span>
                    </h1>
                    <p className="text-base text-gray-300 sm:text-xl lg:text-lg xl:text-xl mt-5">
                      Test stations GUI library for your hardware on a production line
                    </p>
                    <div className="mt-5">
                      <pre className="bg-black rounded text-slate-50 p-2 text-xl w-1/2">
                        <span className="select-none text-gray-400">$ </span>pip install sopic
                      </pre>
                    </div>
                    <div className="mt-5">
                      <a href="https://github.com/Taldrain/sopic" target="_blank" rel="noreferrer" className="text-based font-medium text-gray-300 hover:text-cyan-600">GitHub</a>
                    </div>
                  </div>
                </div>
                <div className="mt-12 -mb-16 sm:-mb-48 lg:relative lg:m-0">
                  <div className="mx-auto max-w-md px-6 sm:max-w-2xl lg:max-w-none lg:px-0">
                    <img
                      className="w-full lg:absolute lg:inset-y-0 lg:left-0 lg:h-full lg:w-auto lg:max-w-none"
                      src={landing}
                      alt=""
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div className="relative pt-16 sm:pt-24 lg:pt-32">
            <div className="mx-auto max-w-md px-6 text-center sm:max-w-3xl lg:px-8">
              <h2 className="text-lg font-semibold text-cyan-600 mb-2">Features</h2>
              <ul className="list-disc text-left max-w-md mx-auto">
                <li>GUI</li>
                <li>Share data between steps</li>
                <li>Settings for step configuration</li>
                <li>Logs</li>
                <li>Easy to customize with wrappers</li>
              </ul>
            </div>
          </div>

          <div className="relative pt-16 sm:pt-24 lg:pt-32">
            <div className="mx-auto max-w-md px-6 text-center sm:max-w-3xl lg:px-8">
              <h2 className="text-lg font-semibold text-cyan-600 mb-2">Step example</h2>
              <div
                dangerouslySetInnerHTML={{
                  __html: `<script src="https://gist.github.com/Taldrain/a23dfbb96344561a070a3f238d6485f4.js"></script>`,
                }}
              />
            </div>
          </div>

          <div className="relative pt-16 sm:pt-24 lg:pt-32">
            <div className="mx-auto max-w-md px-6 text-center sm:max-w-3xl lg:px-8">
              <h2 className="text-lg font-semibold text-cyan-600 mb-2">Station example</h2>
              <div
                dangerouslySetInnerHTML={{
                  __html: `<script src="https://gist.github.com/Taldrain/9db0dc6f6cb8b7628762e8338208ad27.js"></script>`,
                }}
              />
            </div>
          </div>


        </main>

        <footer className="mt-24 bg-gray-900 sm:mt-12">
          <div className="mx-auto max-w-md overflow-hidden py-12 px-6 sm:max-w-3xl lg:max-w-7xl lg:px-8">
            <p className="text-center text-base text-gray-400">
              sopic.taldra.in
            </p>
            <div className="mt-2 flex justify-center space-x-6">
              🙇
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
}
